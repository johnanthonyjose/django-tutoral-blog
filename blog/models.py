from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # Get abosolute url method
    def get_absolute_url(self):
        '''
        Whenever we create a new post, django is looking for the page in which you want to display
        after creating a new post. Currently, it is not yet configured. So we have to do it.
        '''

        # First get url of particular router. We use reverse function
        # We do not use redirect because redirect you specific route
        # Reverse = return the full URL as string
        return reverse('post-detail', kwargs={'pk': self.pk}) #Recall: Post-details needs a parameter

