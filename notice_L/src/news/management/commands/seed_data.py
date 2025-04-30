from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from news.models import Category, Tag, Post, Comment  # Cambio de 'blog' a 'news'
import random
from datetime import timedelta


class Command(BaseCommand):
    """Command to seed the database with sample data"""
    help = 'Seeds the database with sample data for development and testing'
    
    def handle(self, *args, **options):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser... 👤')
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        
        # Create regular user if it doesn't exist
        if not User.objects.filter(username='user').exists():
            self.stdout.write('Creating regular user... 👤')
            User.objects.create_user(
                username='user',
                email='user@example.com',
                password='user123'
            )
        
        # Create categories
        self.stdout.write('Creating categories... 📂')
        categories = [
            ('Programming', 'Posts about programming languages and software development.'),
            ('Data Science', 'Articles related to data analysis, machine learning, and statistics.'),
            ('Web Development', 'Content about web technologies, frameworks, and best practices.'),
            ('DevOps', 'Topics covering deployment, infrastructure, and operations.'),
            ('Career', 'Career advice, industry insights, and professional development.'),
        ]
        
        for name, description in categories:
            Category.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': description
                }
            )
        
        # Create tags
        self.stdout.write('Creating tags... 🏷️')
        tags = [
            'Python', 'JavaScript', 'Django', 'React', 'Docker',
            'APIs', 'Database', 'Security', 'Testing', 'Performance',
            'Git', 'Frontend', 'Backend', 'Cloud', 'Mobile'
        ]
        
        created_tags = []
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            created_tags.append(tag)
        
        # Get users
        admin_user = User.objects.get(username='admin')
        regular_user = User.objects.get(username='user')
        
        # Create posts
        self.stdout.write('Creating posts... 📝')
        post_data = [
            {
                'title': 'Getting Started with Django ORM',
                'content': '''
                Django's Object-Relational Mapping (ORM) is a powerful tool that allows you to interact with your database using Python code instead of raw SQL.
                
                In this post, we'll explore the basics of the Django ORM and how to use it effectively in your projects.
                
                ## Key Features of Django ORM
                
                Django ORM provides several key features that make database interactions simpler:
                
                1. **Model Definition**: Define database tables as Python classes
                2. **QuerySet API**: Intuitive interface for database queries
                3. **Migrations**: Track and apply database schema changes
                4. **Relationship Management**: Easily handle related data
                
                ## Basic Usage
                
                Here's a simple example of how to retrieve data using the Django ORM:
                
                ```python
                # Get all published posts
                published_posts = Post.objects.filter(status='published')
                
                # Get a specific post
                post = Post.objects.get(id=1)
                
                # Get related data
                comments = post.comments.all()
                ```
                
                In future posts, we'll dive deeper into more advanced ORM features like annotations, aggregations, and complex filtering.
                ''',
                'status': 'published',
                'category': 'Programming',
                'tags': ['Python', 'Django', 'Database'],
                'author': admin_user,
            },
            {
                'title': 'Understanding Django Model Relationships',
                'content': '''
                One of the most powerful features of Django's ORM is its ability to define and work with relationships between models.
                
                ## Types of Relationships
                
                Django supports three main types of relationships:
                
                ### One-to-Many (ForeignKey)
                
                The most common type of relationship. For example, a Post has many Comments:
                
                ```python
                class Comment(models.Model):
                    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
                ```
                
                ### Many-to-Many
                
                When records in one table can be related to multiple records in another table, and vice versa. For example, Posts and Tags:
                
                ```python
                class Post(models.Model):
                    tags = models.ManyToManyField(Tag, related_name='posts')
                ```
                
                ### One-to-One
                
                When a record in one table corresponds to exactly one record in another table. For example, User and Profile:
                
                ```python
                class Profile(models.Model):
                    user = models.OneToOneField(User, on_delete=models.CASCADE)
                ```
                
                ## Working with Related Objects
                
                Django makes it easy to navigate relationships in both directions:
                
                ```python
                # Forward (following the relationship)
                comments = post.comments.all()
                
                # Backward (reverse relationship)
                posts = tag.posts.all()
                ```
                
                Understanding these relationships is crucial for designing effective data models and writing efficient queries.
                ''',
                'status': 'published',
                'category': 'Programming',
                'tags': ['Python', 'Django', 'Database'],
                'author': admin_user,
            },
            # Aquí continúas con los demás posts, cambiando el nombre de la categoría y los tags si es necesario
        ]
        
        for data in post_data:
            # Get or create category
            category = Category.objects.get(name=data['category'])
            
            # Set published_at for published posts
            published_at = None
            if data['status'] == 'published':
                published_at = timezone.now() - timedelta(days=random.randint(1, 30))
            
            # Create post
            post, created = Post.objects.get_or_create(
                title=data['title'],
                defaults={
                    'slug': slugify(data['title']),
                    'content': data['content'],
                    'status': data['status'],
                    'author': data['author'],
                    'category': category,
                    'published_at': published_at,
                }
            )
            
            if created:
                # Add tags
                for tag_name in data['tags']:
                    tag = Tag.objects.get(name=tag_name)
                    post.tags.add(tag)
                
                self.stdout.write(f"  Created post: {post.title} ✅")
            else:
                self.stdout.write(f"  Post already exists: {post.title} ℹ️")
        
        # Create comments
        self.stdout.write('Creating comments... 💬')
        
        comment_contents = [
            "Great article! Thanks for sharing this information.",
            "I've been looking for this explanation for a while. Very helpful!",
            "Could you elaborate more on the second point? I'm a bit confused about it.",
            "Looking forward to more content like this. Very insightful!",
            "I think you missed mentioning an important aspect of this topic.",
            "This is exactly what I needed to understand. Thanks!",
            "I'm going to implement this in my project right away!",
            "Well explained with clear examples. Easy to follow.",
        ]
        
        published_posts = Post.objects.filter(status='published')
        for post in published_posts:
            # Create 3-5 random comments per post
            num_comments = random.randint(3, 5)
            for i in range(num_comments):
                comment_content = random.choice(comment_contents)
                author = admin_user if i % 2 == 0 else regular_user
                is_approved = random.choice([True, True, False])  # 2/3 chance of being approved
                
                Comment.objects.get_or_create(
                    post=post,
                    author=author,
                    content=comment_content,
                    defaults={
                        'is_approved': is_approved,
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database! 🎉'))
