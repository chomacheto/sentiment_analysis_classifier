#!/usr/bin/env python3
"""
Command Line Interface for Sentiment Analysis Pipeline.

This module provides a CLI for the sentiment analysis system, allowing users to:
- Analyze single text inputs via command line arguments or stdin
- Process batch files for multiple text analysis
- Get comprehensive help and usage examples
"""

import sys
import click
from pathlib import Path
from typing import Optional, TextIO

# Add the packages directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages"))

from ml_core.sentiment_pipeline import SentimentClassificationPipeline
from ml_core.models import SentimentAnalysis, SentimentAnalysisRequest
from ml_core.validators import validate_text_input


@click.group()
@click.version_option(version="0.1.0", prog_name="sentiment-cli")
@click.help_option("--help", "-h")
def cli():
    """
    Sentiment Analysis CLI - Analyze text sentiment from command line.
    
    This tool provides sentiment analysis capabilities using state-of-the-art
    transformer models. You can analyze single texts or process batch files.
    
    Examples:
        # Analyze a single text
        sentiment-cli analyze "I love this product!"
        
        # Analyze from stdin
        echo "This is amazing!" | sentiment-cli analyze -
        
        # Process a batch file
        sentiment-cli batch input.txt
        
        # Get help for a command
        sentiment-cli analyze --help
    """
    pass


@cli.command()
@click.argument('text', required=False)
@click.option('--model', '-m', default='distilbert-base-uncased-finetuned-sst-2-english',
              help='Hugging Face model to use for sentiment analysis')
@click.option('--output-format', '-f', 
              type=click.Choice(['simple', 'detailed', 'json'], case_sensitive=False),
              default='simple', help='Output format for results')
@click.option('--color/--no-color', default=True, help='Enable/disable color output')
def analyze(text: Optional[str], model: str, output_format: str, color: bool):
    """
    Analyze sentiment of a single text.
    
    TEXT can be provided as an argument or via stdin (use '-' for stdin).
    
    Examples:
        sentiment-cli analyze "I love this product!"
        echo "This is amazing!" | sentiment-cli analyze -
        sentiment-cli analyze --model roberta-base "Mixed feelings about this"
    """
    try:
        # Get text input
        if text == '-':
            # Read from stdin
            if not sys.stdin.isatty():
                text = sys.stdin.read().strip()
            else:
                click.echo("Error: No input provided via stdin", err=True)
                sys.exit(1)
        elif text == "":
            click.echo("Error: Text cannot be empty", err=True)
            sys.exit(1)
        elif not text:
            click.echo("Error: No text provided. Use --help for usage information.", err=True)
            sys.exit(1)
        
        # Validate input
        try:
            validated_text = validate_text_input(text)
        except ValueError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        
        # Initialize pipeline
        pipeline = SentimentClassificationPipeline(model)
        
        # Perform analysis
        result = pipeline.predict(validated_text)
        
        # Display results
        display_sentiment_result(result, output_format, color)
        
        # Exit with success
        sys.exit(0)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--model', '-m', default='distilbert-base-uncased-finetuned-sst-2-english',
              help='Hugging Face model to use for sentiment analysis')
@click.option('--output-format', '-f', 
              type=click.Choice(['simple', 'detailed', 'json'], case_sensitive=False),
              default='simple', help='Output format for results')
@click.option('--delimiter', '-d', default='\n', help='Delimiter for separating texts in file')
@click.option('--output-file', '-o', type=click.Path(path_type=Path), 
              help='Output file for results (default: stdout)')
def batch(file_path: Path, model: str, output_format: str, delimiter: str, output_file: Optional[Path]):
    """
    Process multiple texts from a file for batch sentiment analysis.
    
    FILE_PATH should contain texts separated by the specified delimiter.
    
    Examples:
        sentiment-cli batch input.txt
        sentiment-cli batch data.csv --delimiter ',' --output-file results.txt
        sentiment-cli batch reviews.txt --output-format json
    """
    try:
        # Read and validate file
        if not file_path.exists():
            click.echo(f"Error: File {file_path} does not exist", err=True)
            sys.exit(1)
        
        if file_path.stat().st_size == 0:
            click.echo(f"Error: File {file_path} is empty", err=True)
            sys.exit(1)
        
        # Read texts from file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                texts = [text.strip() for text in content.split(delimiter) if text.strip()]
        except Exception as e:
            click.echo(f"Error reading file {file_path}: {str(e)}", err=True)
            sys.exit(1)
        
        if not texts:
            click.echo(f"Error: No valid texts found in {file_path}", err=True)
            sys.exit(1)
        
        # Initialize pipeline
        pipeline = SentimentClassificationPipeline(model)
        
        # Process texts
        results = []
        for i, text in enumerate(texts, 1):
            try:
                validated_text = validate_text_input(text)
                result = pipeline.predict(validated_text)
                result['text_index'] = i
                result['input_text'] = text
                results.append(result)
            except Exception as e:
                click.echo(f"Warning: Failed to process text {i}: {str(e)}", err=True)
                continue
        
        if not results:
            click.echo("Error: No texts were successfully processed", err=True)
            sys.exit(1)
        
        # Display batch results
        display_batch_results(results, output_format, output_file)
        
        # Exit with success
        sys.exit(0)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def info():
    """
    Display information about the sentiment analysis system.
    
    Shows model information, system status, and available options.
    """
    try:
        pipeline = SentimentClassificationPipeline()
        model_info = pipeline.get_model_info()
        
        click.echo("Sentiment Analysis CLI - System Information")
        click.echo("=" * 50)
        click.echo(f"Model: {model_info.get('model_name', 'Unknown')}")
        click.echo(f"Type: {model_info.get('model_type', 'Unknown')}")
        click.echo(f"Framework: {model_info.get('framework', 'Unknown')}")
        click.echo(f"Device: {model_info.get('device', 'Unknown')}")
        click.echo(f"Status: {model_info.get('status', 'Unknown')}")
        click.echo()
        click.echo("Available Commands:")
        click.echo("  analyze  - Analyze single text sentiment")
        click.echo("  batch    - Process multiple texts from file")
        click.echo("  info     - Show system information")
        click.echo()
        click.echo("Use --help with any command for detailed usage information.")
        
        sys.exit(0)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def display_sentiment_result(result: dict, output_format: str, color: bool):
    """Display sentiment analysis result in the specified format."""
    if output_format == 'json':
        import json
        click.echo(json.dumps(result, indent=2))
        return
    
    # Color codes for different sentiment labels
    colors = {
        'positive': 'green',
        'negative': 'red',
        'neutral': 'yellow'
    }
    
    sentiment = result['sentiment_label']
    confidence = result['confidence_score']
    processing_time = result['processing_time_ms']
    
    if output_format == 'detailed':
        click.echo("Sentiment Analysis Results")
        click.echo("=" * 30)
        click.echo(f"Sentiment: {sentiment}")
        click.echo(f"Confidence: {confidence:.4f}")
        click.echo(f"Processing Time: {processing_time:.2f}ms")
        click.echo(f"Text Length: {result.get('input_text_length', 'N/A')}")
    else:  # simple format
        if color:
            click.echo(f"{sentiment.upper()}: {confidence:.4f} ({processing_time:.2f}ms)", 
                      color=colors.get(sentiment, 'white'))
        else:
            click.echo(f"{sentiment.upper()}: {confidence:.4f} ({processing_time:.2f}ms)")


def display_batch_results(results: list, output_format: str, output_file: Optional[Path]):
    """Display batch processing results."""
    if output_format == 'json':
        import json
        output_data = {
            'total_processed': len(results),
            'results': results,
            'summary': {
                'positive': len([r for r in results if r['sentiment_label'] == 'positive']),
                'negative': len([r for r in results if r['sentiment_label'] == 'negative']),
                'neutral': len([r for r in results if r['sentiment_label'] == 'neutral'])
            }
        }
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, default=str)
            click.echo(f"Results saved to {output_file}")
        else:
            click.echo(json.dumps(output_data, indent=2, default=str))
        return
    
    # Simple/detailed format
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                sentiment = result['sentiment_label']
                confidence = result['confidence_score']
                processing_time = result['processing_time_ms']
                text_index = result.get('text_index', 'N/A')
                
                if output_format == 'detailed':
                    f.write(f"Text {text_index}: {sentiment.upper()} (confidence: {confidence:.4f}, time: {processing_time:.2f}ms)\n")
                else:
                    f.write(f"{sentiment.upper()}: {confidence:.4f} ({processing_time:.2f}ms)\n")
        
        click.echo(f"Results saved to {output_file}")
    else:
        # Display to stdout
        for result in results:
            sentiment = result['sentiment_label']
            confidence = result['confidence_score']
            processing_time = result['processing_time_ms']
            text_index = result.get('text_index', 'N/A')
            
            if output_format == 'detailed':
                click.echo(f"Text {text_index}: {sentiment.upper()} (confidence: {confidence:.4f}, time: {processing_time:.2f}ms)")
            else:
                click.echo(f"{sentiment.upper()}: {confidence:.4f} ({processing_time:.2f}ms)")
    
    # Summary
    positive_count = len([r for r in results if r['sentiment_label'] == 'positive'])
    negative_count = len([r for r in results if r['sentiment_label'] == 'negative'])
    neutral_count = len([r for r in results if r['sentiment_label'] == 'neutral'])
    
    click.echo(f"\nSummary: {len(results)} texts processed")
    click.echo(f"Positive: {positive_count}, Negative: {negative_count}, Neutral: {neutral_count}")


if __name__ == '__main__':
    cli()
