from UtilFunctions import *


# TODO: Improve exiting try catch, to prevent future crashes on deleted users...


def createMoreData():
    reddit = connectToAPI()  # clear - works
    new_subreddit = getNewSubreddit(reddit, 500)
    submissionDF = loadData()  # clear - dataframe works

    unique_names = getNames(submissionDF, new_subreddit)  # clear - works

    print(len(unique_names))

    if len(unique_names) == 0:
        print("Going to sleep")
        time.sleep(60 * 20)
        print("Waking up")
        createMoreData()  # clear - works
    else:

        topics_dict = {
            "_submission_id": [],
            "_title": [],
            "_score": [],
            "_num_comments": [],
            "_title_length": [],
            "_subreddit": [],
            "_post_text": [],
            "_comment_karma": [],
            "_link_karma": [],
            "_upvote_ratio": [],
            "_date_created": [],
            "_user_name": [],
        }

        for curr_id in unique_names:
            print(curr_id)
            try:
                for submission in reddit.redditor(str(curr_id)).submissions.new():
                    userName = str(submission.author)
                    topics_dict['_submission_id'].append(submission.id)
                    topics_dict['_title'].append(submission.title)
                    topics_dict['_score'].append(submission.score)
                    topics_dict['_num_comments'].append(submission.num_comments)
                    topics_dict['_title_length'].append(len(submission.title))
                    topics_dict['_subreddit'].append(submission.subreddit)
                    topics_dict['_post_text'].append(submission.selftext)
                    topics_dict['_link_karma'].append(reddit.redditor(userName).link_karma)
                    topics_dict['_upvote_ratio'].append(submission.upvote_ratio)
                    topics_dict['_date_created'].append(submission.created_utc)
                    topics_dict['_user_name'].append(submission.author)
                    topics_dict['_comment_karma'].append(reddit.redditor(userName).comment_karma)
            except Exception:
                print("Error occured with id:{}".format(str(curr_id)))

        topics_dict = pd.DataFrame(data=topics_dict)

        print("Entering Part 2")
        topics_dict = topics_dict[['_submission_id', '_title', '_score', '_num_comments',
                                   '_title_length', '_subreddit', '_post_text', '_comment_karma',
                                   '_link_karma', '_upvote_ratio', '_date_created', '_user_name']]
        topics_dict = createMoreFeatures(topics_dict)
        topics_dict = pd.concat([topics_dict, submissionDF], sort=False)
        topics_dict = topics_dict.fillna('')

        topics_dict.to_csv('SubmissionsDF2.csv')


createMoreData()