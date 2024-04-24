import praw
import datetime
import helper as hp


class RedditBot:

    def __init__(self):
        self.config = hp.read_json("./config.json")
        self.reddit = praw.Reddit(
            client_id = self.config["reddit"]["client_id"],
            client_secret = self.config["reddit"]["client_secret"],
            password = self.config["reddit"]["password"],
            user_agent = self.config["reddit"]["user_agent"],
            username = self.config["reddit"]["username"],
        )
        self.con, self.cursor = hp.get_db(self.config)
        #self.cursor = hp.get_db(self.config)

    def printTitles(self, subreddit, method, timefilter, limit, update=False):
        subreddit_name = subreddit
        self.subreddit = self.reddit.subreddit(subreddit_name)
        #subreddit = getattr(subreddit_obj, method)

        if method == "top":
            submission_generator = self.subreddit.top(time_filter=timefilter, limit=limit)
        elif method == "new":
            submission_generator = self.subreddit.new(limit=limit)
        elif method == "hot":
            submission_generator = self.subreddit.hot(limit=limit)


        for submission in submission_generator:
            post = {
                "id": str(submission.id),
                "author": str(submission.author if submission.author else None),
                "author_id": str(submission.author.id if submission.author else None),
                "subreddit_id": str(submission.subreddit.id if submission.subreddit.id else None),
                "subreddit_title": str(submission.subreddit.display_name if submission.subreddit.display_name else None),
                "title": str(submission.title if submission.title else None),
                "comments_count": len(submission.comments.list()) if submission.comments.list() else None,
                "score": submission.score if submission.score else None,
                "upvote_ratio": submission.upvote_ratio if submission.upvote_ratio else None,
                "created_utc": datetime.datetime.fromtimestamp(submission.created_utc) if datetime.datetime.fromtimestamp(submission.created_utc) else None,
                "marked_nsfw": submission.over_18 if submission.created_utc else None,
                "post_body": str(submission.selftext if submission.selftext else None),
                "url": str(submission.url if submission.url else None)
            }

            print(f"\nAuthor and ID: {post['author']}, {post['author_id']}\n"
                  f"Comments: {post['comments_count']}\n"
                  f"Score: {post['score']}\n"
                  f"Title: {post['title']}, \n"
                  f"Marked NSFW: {post['marked_nsfw']}\n"
                  f"Upvote ratio: {post['upvote_ratio']}\n"
                  f"Subreddit ID and Title: {post['subreddit_id']}, {post['subreddit_title']}\n"
                  f"Post Body: {post['post_body']}\n"
                  f"url: {post['url']}\n"
            )

        if update:
            sql_insert_statement = """
                INSERT INTO reddit_posts 
                (id, author, author_id, subreddit_id, subreddit_title, title, num_of_comments, score, upvote_ratio, created_utc, nsfw, selftext, url) 
                VALUES 
                (%(id)s, %(author)s, %(author_id)s, %(subreddit_id)s, %(subreddit_title)s, %(title)s, %(comments_count)s, %(score)s, %(upvote_ratio)s, %(created_utc)s, %(marked_nsfw)s, %(post_body)s, %(url)s)
                ON DUPLICATE KEY UPDATE
                author=VALUES(author),
                author_id=VALUES(author_id),
                subreddit_id=VALUES(subreddit_id),
                subreddit_title=VALUES(subreddit_title),
                title=VALUES(title),
                num_of_comments=VALUES(num_of_comments),
                score=VALUES(score),
                upvote_ratio=VALUES(upvote_ratio),
                created_utc=VALUES(created_utc),
                nsfw=VALUES(nsfw),
                selftext=VALUES(selftext),
                url=VALUES(url)
            """
            self.cursor.execute(sql_insert_statement, post)
            self.con.commit()

rb = RedditBot()
rb.printTitles("python", method="hot", timefilter="all",  limit=5, update=True)
