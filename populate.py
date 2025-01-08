import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_project.settings')
import django
django.setup()

# Fake pop script
import random
from main.models import Post, Comment
from profile_app.models import Profile
from django.contrib.auth.models import User
from faker import Faker
import numpy as np
#from django.utils.timezone import make_aware

fakegen = Faker()

def add_users(num_user=10, seed=None):
    np.random.seed(seed)

    #add profile to superuser if exists:
    try:
        u1 = User.objects.get(id=1)
        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        age = random.randint(18, 100)
        p = Profile.objects.get_or_create(user = u1, gender = gender, age = age)[0]
        p.save()
    except:
        print("Superuser doesn't exist ! Please make one !")
    
    #add fake users and make a profile to each one of them:       
    names = [fakegen.unique.first_name() for _ in range(10)]
    for i in range(num_user):
        usrname = names[i]
        print(usrname)

        pwd = fakegen.password()
        djangoU = User.objects.create_user(username=usrname, password=pwd)
        
        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        age = random.randint(18, 100)
        
        p = Profile.objects.get_or_create(user = djangoU, gender = gender, age = age)[0]
        p.save()
    return

def add_posts(post_per_user=4, seed=None):
    fakegen.seed_instance(seed)
    
    for i in range(len(User.objects.all())):
        djangoU = User.objects.get(pk=i+1)
        for j in range(post_per_user):
            title = fakegen.paragraph(nb_sentences=1)
            text = fakegen.paragraph(nb_sentences=10)
            slug = f"{djangoU.username}-post-{j}"

            p = Post.objects.get_or_create(author = djangoU, title=title, body = text, slug = slug)[0]
            p.save()

def add_comments(seed=None):
    fakegen.seed_instance(seed)
    
    for i in range(len(User.objects.all())):
        djangoU = User.objects.get(pk=i+1)
        for j in range(len(Post.objects.all())):
            post = Post.objects.get(id=j+1)
            body = fakegen.paragraph(nb_sentences=2)
            c = Comment.objects.get_or_create(post=post, author = djangoU, body = body)[0]
            c.save()

if __name__ == '__main__':
    print("populating script!")
    add_users()
    add_posts()
    add_comments()
    print("populating complete!")