"""
Docker functionality tests for Sentiment Analysis Classifier.

Tests container build, CLI integration, and performance requirements.
"""

import pytest
import subprocess
import time
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestDockerBuild:
    """Test Docker build functionality and optimization."""
    
    def test_dockerfile_exists(self):
        """Test that Dockerfile exists and is properly formatted."""
        dockerfile_path = Path("Dockerfile")
        assert dockerfile_path.exists(), "Dockerfile should exist at project root"
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
            
        # Verify multi-stage build
        assert "FROM python:3.11-slim as builder" in content, "Should use Python 3.11+ base image"
        assert "FROM python:3.11-slim as runtime" in content, "Should have runtime stage"
        assert "COPY --from=builder" in content, "Should copy from builder stage"
        
        # Verify Poetry installation
        assert "RUN pip install poetry" in content, "Should install Poetry"
        assert "poetry config virtualenvs.create false" in content, "Should configure Poetry for containers"
        
        # Verify security features
        assert "RUN groupadd -r appuser" in content, "Should create non-root user"
        assert "USER appuser" in content, "Should switch to non-root user"
        
        # Verify CLI integration
        assert "ENTRYPOINT" in content, "Should have entrypoint for CLI"
        assert "apps.ml_pipeline.cli" in content, "Should use existing CLI from Story 1.3"

    def test_dockerignore_exists(self):
        """Test that .dockerignore exists and excludes unnecessary files."""
        dockerignore_path = Path(".dockerignore")
        assert dockerignore_path.exists(), ".dockerignore should exist"
        
        with open(dockerignore_path, 'r') as f:
            content = f.read()
            
        # Verify key exclusions
        assert "tests/" in content, "Should exclude tests directory"
        assert "docs/" in content, "Should exclude documentation"
        assert "venv/" in content, "Should exclude virtual environments"
        assert "__pycache__" in content, "Should exclude Python cache"

    @pytest.mark.integration
    def test_docker_build_success(self):
        """Test that Docker build completes successfully."""
        try:
            result = subprocess.run(
                ["docker", "build", "--target", "runtime", "-t", "test-sentiment-classifier", "."],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            assert result.returncode == 0, f"Build failed: {result.stderr}"
        except subprocess.TimeoutExpired:
            pytest.fail("Docker build timed out after 5 minutes")
        finally:
            # Clean up test image
            subprocess.run(["docker", "rmi", "test-sentiment-classifier"], 
                         capture_output=True, check=False)

    @pytest.mark.integration
    def test_image_size_requirement(self):
        """Test that final image size is under 2GB."""
        try:
            # Build image
            subprocess.run(
                ["docker", "build", "--target", "runtime", "-t", "test-size-check", "."],
                capture_output=True,
                check=True,
                timeout=300
            )
            
            # Get image size
            result = subprocess.run(
                ["docker", "images", "test-size-check", "--format", "{{.Size}}"],
                capture_output=True,
                text=True,
                check=True
            )
            
            size_str = result.stdout.strip()
            
            # Parse size (e.g., "1.2GB", "800MB")
            if "GB" in size_str:
                size_gb = float(size_str.replace("GB", ""))
            elif "MB" in size_str:
                size_mb = float(size_str.replace("MB", ""))
                size_gb = size_mb / 1024
            else:
                size_gb = float(size_str)
                
            assert size_gb < 2.0, f"Image size {size_gb}GB exceeds 2GB requirement"
            
        finally:
            # Clean up
            subprocess.run(["docker", "rmi", "test-size-check"], 
                         capture_output=True, check=False)


class TestDockerCompose:
    """Test Docker Compose configuration."""
    
    def test_docker_compose_exists(self):
        """Test that docker-compose.yml exists and is properly configured."""
        compose_path = Path("docker-compose.yml")
        assert compose_path.exists(), "docker-compose.yml should exist"
        
        with open(compose_path, 'r') as f:
            content = f.read()
            
        # Verify service configuration
        assert "sentiment-classifier:" in content, "Should have main service"
        assert "sentiment-classifier-dev:" in content, "Should have development service"
        
        # Verify volume mounts
        assert "./packages:/app/packages" in content, "Should mount packages directory"
        assert "./apps:/app/apps" in content, "Should mount apps directory"
        assert "model-cache:/app/.cache/huggingface" in content, "Should mount model cache"
        
        # Verify environment variables
        assert "PYTHONPATH=/app" in content, "Should set Python path"
        assert "LOG_LEVEL" in content, "Should configure logging level"
        
        # Verify health checks
        assert "healthcheck:" in content, "Should have health checks"
        assert "apps.ml_pipeline.cli" in content, "Should use CLI for health check"

    def test_development_profile(self):
        """Test that development profile is properly configured."""
        compose_path = Path("docker-compose.yml")
        
        with open(compose_path, 'r') as f:
            content = f.read()
            
        # Verify development service configuration
        assert "DEVELOPMENT_MODE=true" in content, "Should enable development mode"
        assert "profiles:" in content, "Should have profiles configuration"
        assert "- dev" in content, "Should have dev profile"


class TestCLIIntegration:
    """Test CLI integration in containerized environment."""
    
    @pytest.mark.integration
    def test_container_cli_help(self):
        """Test that container CLI help command works."""
        try:
            # Build test image
            subprocess.run(
                ["docker", "build", "--target", "runtime", "-t", "test-cli", "."],
                capture_output=True,
                check=True,
                timeout=300
            )
            
            # Test help command
            result = subprocess.run(
                ["docker", "run", "--rm", "test-cli", "--help"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Verify CLI output
            assert "Usage:" in result.stdout, "Should show CLI usage"
            assert "analyze" in result.stdout, "Should show analyze command"
            assert "batch" in result.stdout, "Should show batch command"
            assert "info" in result.stdout, "Should show info command"
            
        finally:
            # Clean up
            subprocess.run(["docker", "rmi", "test-cli"], 
                         capture_output=True, check=False)

    @pytest.mark.integration
    def test_container_cli_info(self):
        """Test that container CLI info command works."""
        try:
            # Build test image
            subprocess.run(
                ["docker", "build", "--target", "runtime", "-t", "test-info", "."],
                capture_output=True,
                check=True,
                timeout=300
            )
            
            # Test info command
            result = subprocess.run(
                ["docker", "run", "--rm", "test-info", "info"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Verify info output
            assert "Sentiment Analysis Classifier" in result.stdout, "Should show system info"
            
        finally:
            # Clean up
            subprocess.run(["docker", "rmi", "test-info"], 
                         capture_output=True, check=False)


class TestPerformanceRequirements:
    """Test performance requirements including startup time."""
    
    @pytest.mark.integration
    def test_container_startup_time(self):
        """Test that container startup time is under 30 seconds."""
        container_name = "test-startup-container"  # Define at function level
        
        try:
            # Build test image
            subprocess.run(
                ["docker", "build", "--target", "runtime", "-t", "test-startup", "."],
                capture_output=True,
                check=True,
                timeout=300
            )
            
            # Measure startup time
            start_time = time.time()
            
            # Start container and wait for it to be ready
            
            # Start container
            subprocess.run(
                ["docker", "run", "-d", "--name", container_name, "test-startup"],
                capture_output=True,
                check=True
            )
            
            # Wait for container to be ready (health check)
            max_wait = 35  # Allow 5 seconds over requirement
            ready = False
            
            for _ in range(max_wait):
                try:
                    # Check if container is running
                    result = subprocess.run(
                        ["docker", "inspect", container_name, "--format", "{{.State.Status}}"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    if result.stdout.strip() == "running":
                        # Test if CLI is responsive
                        cli_result = subprocess.run(
                            ["docker", "exec", container_name, "python", "-m", "apps.ml_pipeline.cli", "--help"],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                        
                        if cli_result.returncode == 0:
                            ready = True
                            break
                            
                except subprocess.TimeoutExpired:
                    pass
                    
                time.sleep(1)
            
            end_time = time.time()
            startup_time = end_time - start_time
            
            assert ready, "Container should be ready within startup time limit"
            assert startup_time < 30, f"Startup time {startup_time:.2f}s exceeds 30 second requirement"
            
        finally:
            # Clean up
            subprocess.run(["docker", "rm", "-f", container_name], 
                         capture_output=True, check=False)
            subprocess.run(["docker", "rmi", "test-startup"], 
                         capture_output=True, check=False)


class TestScripts:
    """Test Docker utility scripts."""
    
    def test_build_script_exists(self):
        """Test that build script exists and is executable."""
        build_script = Path("scripts/docker/build.sh")
        assert build_script.exists(), "Build script should exist"
        assert os.access(build_script, os.X_OK), "Build script should be executable"

    def test_run_script_exists(self):
        """Test that run script exists and is executable."""
        run_script = Path("scripts/docker/run.sh")
        assert run_script.exists(), "Run script should exist"
        assert os.access(run_script, os.X_OK), "Run script should be executable"

    def test_scripts_directory_structure(self):
        """Test that scripts directory has proper structure."""
        scripts_dir = Path("scripts/docker")
        assert scripts_dir.exists(), "Docker scripts directory should exist"
        assert scripts_dir.is_dir(), "Should be a directory"


class TestDocumentation:
    """Test that documentation is complete and accurate."""
    
    def test_deployment_docs_exist(self):
        """Test that deployment documentation exists."""
        docs_path = Path("docs/deployment/docker-setup.md")
        assert docs_path.exists(), "Docker setup documentation should exist"
        
        with open(docs_path, 'r') as f:
            content = f.read()
            
        # Verify key sections
        assert "## Quick Start" in content, "Should have quick start section"
        assert "## Troubleshooting" in content, "Should have troubleshooting section"
        assert "## Best Practices" in content, "Should have best practices section"
        
        # Verify CLI examples
        assert "docker run --rm sentiment-classifier:latest" in content, "Should have CLI examples"
        assert "docker-compose up -d" in content, "Should have Docker Compose examples"


if __name__ == "__main__":
    pytest.main([__file__])
