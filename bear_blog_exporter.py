#!/usr/bin/env python3
"""
Bear Blog CSV to Markdown Files Exporter

This script reads a Bear blog CSV export and creates individual Markdown files
for each post with proper frontmatter and content formatting.
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path


def sanitize_filename(filename):
    """
    Sanitize a string to be safe for use as a filename.
    Removes or replaces problematic characters.
    """
    # Replace spaces with hyphens and remove problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\s+', '-', filename)
    # Remove multiple consecutive hyphens
    filename = re.sub(r'-+', '-', filename)
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    return filename


def format_date(date_str):
    """
    Format date string for frontmatter.
    Handles various date formats from the CSV.
    """
    if not date_str or date_str == 'null':
        return None
    
    try:
        # Parse ISO format date
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
        else:
            # Try parsing other common formats
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime('%Y-%m-%d')
    except ValueError:
        return date_str


def parse_tags(tags_str):
    """
    Parse tags from the CSV format to a list.
    """
    if not tags_str or tags_str == '[]':
        return []
    
    # Remove brackets and split by comma
    tags_str = tags_str.strip('[]')
    if not tags_str:
        return []
    
    # Split by comma and clean up
    tags = [tag.strip().strip('"\'') for tag in tags_str.split(',')]
    return [tag for tag in tags if tag]


def create_frontmatter(post):
    """
    Create YAML frontmatter for the Markdown file.
    """
    frontmatter_lines = ['---']
    
    # Title
    if post.get('title'):
        frontmatter_lines.append(f'title: "{post["title"]}"')
    
    # Date
    published_date = format_date(post.get('published date'))
    if published_date:
        frontmatter_lines.append(f'date: {published_date}')
    
    # Slug
    if post.get('slug'):
        frontmatter_lines.append(f'slug: {post["slug"]}')
    
    # Tags
    tags = parse_tags(post.get('all tags', ''))
    if tags:
        frontmatter_lines.append('tags:')
        for tag in tags:
            frontmatter_lines.append(f'  - {tag}')
    
    # Published status
    if post.get('publish') == 'True':
        frontmatter_lines.append('published: true')
    else:
        frontmatter_lines.append('published: false')
    
    # Discoverable status
    if post.get('make discoverable') == 'True':
        frontmatter_lines.append('discoverable: true')
    else:
        frontmatter_lines.append('discoverable: false')
    
    # Meta description
    if post.get('meta description'):
        frontmatter_lines.append(f'description: "{post["meta description"]}"')
    
    # Canonical URL
    if post.get('canonical url'):
        frontmatter_lines.append(f'canonical_url: {post["canonical url"]}')
    
    # Language
    if post.get('lang'):
        frontmatter_lines.append(f'lang: {post["lang"]}')
    
    # Page type
    if post.get('is page') == 'True':
        frontmatter_lines.append('type: page')
    else:
        frontmatter_lines.append('type: post')
    
    frontmatter_lines.append('---')
    frontmatter_lines.append('')  # Empty line after frontmatter
    
    return '\n'.join(frontmatter_lines)


def export_posts_to_markdown(csv_file_path, output_dir='exported_posts'):
    """
    Main function to export Bear blog posts to Markdown files.
    
    Args:
        csv_file_path (str): Path to the Bear blog CSV export
        output_dir (str): Directory to save the Markdown files
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    exported_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            # Use csv.DictReader to handle CSV parsing
            reader = csv.DictReader(csvfile)
            
            for post in reader:
                # Skip posts without content
                if not post.get('content'):
                    print(f"Skipping post '{post.get('title', 'Untitled')}' - no content")
                    continue
                
                # Generate filename
                title = post.get('title', 'untitled')
                slug = post.get('slug', '')
                
                # Use slug if available, otherwise use title
                if slug:
                    filename = sanitize_filename(slug)
                else:
                    filename = sanitize_filename(title)
                
                # Ensure filename is not empty and add .md extension
                if not filename:
                    filename = f"post_{post.get('uid', exported_count)}"
                
                filename = f"{filename}.md"
                
                # Create the full Markdown content
                frontmatter = create_frontmatter(post)
                content = post['content']
                
                # Combine frontmatter and content
                markdown_content = frontmatter + content
                
                # Write to file
                file_path = output_path / filename
                
                # Handle duplicate filenames
                counter = 1
                original_filename = filename
                while file_path.exists():
                    name, ext = os.path.splitext(original_filename)
                    filename = f"{name}_{counter}{ext}"
                    file_path = output_path / filename
                    counter += 1
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                print(f"Exported: {filename}")
                exported_count += 1
    
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
        return
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return
    
    print(f"\nExport complete! {exported_count} posts exported to '{output_dir}' directory.")


if __name__ == "__main__":
    # Configuration
    CSV_FILE = "post_export.csv"  # Change this to your CSV file path
    OUTPUT_DIR = "exported_posts"  # Change this to your desired output directory
    
    print("Bear Blog to Markdown Exporter")
    print("=" * 40)
    
    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"CSV file '{CSV_FILE}' not found in current directory.")
        print("Please make sure the file exists or update the CSV_FILE variable.")
    else:
        export_posts_to_markdown(CSV_FILE, OUTPUT_DIR)
