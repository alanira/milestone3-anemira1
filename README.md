# milestone3-anemira1

# Explains how someone who clones the repository can set up and run your project locally (what to install, any extra files to add)

1. clone GitHub repo to your local repository on your local machine
2. get account at TMDB and apply for your own API key
5. create .env file inside clonned repository and create a variable named TMDB_KEY; assign API key as a value in " " to the TMDB_KEY and save .env file
6. create variables export DATABASE_URL='', secret_key
3. run 'npm ci' in that directory to pull in all the node packages you need. Note: 'npm ci' might produce a bunch of warnings, but it's okay to ignore it.
4. To run the code, run 'npm run build' and then 'python3 app.py', and type in your browser localhost:5000
9. enjoy the web app and try to use a link which will lead you to the wiki page about a movie
10. use login functionality and username/password (hashing for the password implemented using hashing function and md5 algorithm)

# What are at least 3 technical issues you encountered with your project milestone? How did you fix them? 
1. It was kind of tricky to start milestone3: as I tried to merge project-milestone2 and HW7. The app crashed several times as it was a problem to display React page and fix some routes and set up correctly. Once I fixed route issue it started to work.
2. I found that I did not enjoy to code in Javascript, in general. Just can not relate myself to this language. Just coded :) No specific advice here :)
3. As I mentioned before that is not easy to work with more advanced functions as Flask-login. To find a way around it it's possible, but it will take some extra time to work on. I organized login and password functionality in different manner and I could not re-use it for milestone 3. This is why my app gives all comments on React page: it is not possible to specify comment for each single user.

# What was the hardest part of the project for you, across all milestones? 
Overall, I can say it was a good experience and it was much harder than I expected. I layered milestone3 on project-milestone2, which is was not easy. I am not sure that I feel confident to work as full-stack developer. For me, it looks like to merge different codes into one single piece and adding functionality on-the-go was not an easy task.
# What is the most useful thing you learned, across all milestones?
It was completely a new experince for me, so I learned a lot :)
