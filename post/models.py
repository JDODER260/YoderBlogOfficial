from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=200, unique=False)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, default='uncategorized')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    background_img = models.ImageField(default='background.png',
                                       upload_to='post_backgrounds')

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.background_img.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.background_img.path)

    def __str__(self):
        return str(self.title) + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


user1232 = User.objects.all().first()


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.author)
