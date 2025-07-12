"""
MkDocs Macros for Dynamic Content Generation
Provides dynamic content generation and git tag synchronization
"""

import os
import subprocess
import yaml
from datetime import datetime


def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """
    
    @env.macro
    def get_git_tag():
        """Get the latest git tag"""
        try:
            result = subprocess.run(
                ['git', 'describe', '--tags', '--abbrev=0'],
                capture_output=True,
                text=True,
                cwd=env.project_dir
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "v1.0.0"  # fallback
        except Exception:
            return "v1.0.0"  # fallback
    
    @env.macro
    def get_commit_hash():
        """Get the current commit hash (short)"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--short', 'HEAD'],
                capture_output=True,
                text=True,
                cwd=env.project_dir
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "unknown"
        except Exception:
            return "unknown"
    
    @env.macro
    def get_branch_name():
        """Get the current git branch name"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                cwd=env.project_dir
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "main"
        except Exception:
            return "main"
    
    @env.macro
    def load_metadata():
        """Load metadata from .metadata.yaml file"""
        metadata_path = os.path.join(env.project_dir, '.metadata.yaml')
        try:
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f)
            
            # Sync version with git tag
            git_tag = get_git_tag()
            metadata['version'] = git_tag
            
            return metadata
        except Exception as e:
            # Return default metadata if file doesn't exist
            return {
                'version': get_git_tag(),
                'version_name': 'Current',
                'release_date': datetime.now().strftime('%Y-%m-%d'),
                'project': {
                    'name': 'Documentation Project',
                    'repository': 'https://github.com/yourusername/your-project',
                    'documentation': 'https://yourusername.github.io/your-project/'
                }
            }
    
    @env.macro
    def version_info():
        """Generate version information block"""
        metadata = load_metadata()
        git_tag = get_git_tag()
        commit_hash = get_commit_hash()
        branch_name = get_branch_name()
        
        return f"""!!! info "Version Information"
    **Version:** {git_tag}  
    **Release:** {metadata.get('version_name', 'Current')}  
    **Branch:** {branch_name}  
    **Repository:** [GitHub]({metadata['project']['repository']})  
    **Documentation:** [Latest]({metadata['project']['documentation']})  
    **Commit:** {commit_hash}"""
    
    @env.macro
    def project_stats():
        """Generate project statistics"""
        metadata = load_metadata()
        metrics = metadata.get('metrics', {})
        
        stats = []
        if 'total_documents' in metrics:
            stats.append(f"**{metrics['total_documents']}** Documents")
        if 'total_pages' in metrics:
            stats.append(f"**{metrics['total_pages']}** Pages")
        if 'total_sections' in metrics:
            stats.append(f"**{metrics['total_sections']}** Sections")
        if 'documentation_lines' in metrics:
            stats.append(f"**{metrics['documentation_lines']}** Lines of Documentation")
        
        return " • ".join(stats) if stats else "No statistics available"
    
    @env.macro
    def release_notes():
        """Generate release notes from metadata"""
        metadata = load_metadata()
        release = metadata.get('release', {})
        
        notes = []
        
        if 'major_features' in release:
            notes.append("### 🚀 Major Features")
            for feature in release['major_features']:
                notes.append(f"- {feature}")
            notes.append("")
        
        if 'improvements' in release:
            notes.append("### 🔧 Improvements")
            for improvement in release['improvements']:
                notes.append(f"- {improvement}")
            notes.append("")
        
        if 'bug_fixes' in release:
            notes.append("### 🐛 Bug Fixes")
            for fix in release['bug_fixes']:
                notes.append(f"- {fix}")
        
        return "\n".join(notes) if notes else "No release notes available"
    
    @env.macro
    def project_info():
        """Generate project information block"""
        metadata = load_metadata()
        project = metadata.get('project', {})
        
        return f"""!!! note "Project Information"
    **Name:** {project.get('name', 'Documentation Project')}  
    **Description:** {project.get('description', 'Project documentation')}  
    **Last Updated:** {datetime.now().strftime('%Y-%m-%d')}  
    **Build Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    @env.macro
    def build_info():
        """Generate build information"""
        metadata = load_metadata()
        git_tag = get_git_tag()
        commit_hash = get_commit_hash()
        branch_name = get_branch_name()
        build_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return f"""
| Field | Value |
|-------|-------|
| Version | {git_tag} |
| Branch | {branch_name} |
| Commit | {commit_hash} |
| Build Date | {build_date} |
| Release Date | {metadata.get('release_date', 'N/A')} |
"""
    
    @env.macro
    def contributors():
        """Generate contributors list from git log"""
        try:
            result = subprocess.run(
                ['git', 'log', '--format=%an <%ae>', '--reverse'],
                capture_output=True,
                text=True,
                cwd=env.project_dir
            )
            if result.returncode == 0:
                contributors = list(set(result.stdout.strip().split('\n')))
                contributors = [c for c in contributors if c.strip()]
                return "\n".join([f"- {contributor}" for contributor in contributors])
            else:
                return "No contributors found"
        except Exception:
            return "Unable to retrieve contributors"
    
    @env.macro
    def last_updated():
        """Get last updated date from git"""
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%cd', '--date=short'],
                capture_output=True,
                text=True,
                cwd=env.project_dir
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return datetime.now().strftime('%Y-%m-%d')
        except Exception:
            return datetime.now().strftime('%Y-%m-%d')
    
    # Environment variables for templates (avoid conflicts with functions)
    metadata_obj = load_metadata()
    env.variables['git_tag'] = get_git_tag()
    env.variables['commit_hash'] = get_commit_hash()
    env.variables['branch_name'] = get_branch_name()
    env.variables['metadata'] = metadata_obj
    env.variables['build_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    env.variables['build_timestamp'] = datetime.now().isoformat()
