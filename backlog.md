## Backlog

Priorities:

will be done this week *** (first sprint)

will be done next week ** (first sprint)

may be completed in this sprint, but not a priority *

**Theme I:**

Create the model and test it, to ensure it will meet the machine learning performance metric and be deployable

-	Epic 1: Download Data and Create Full dataset for model
    *	(1 point) *** Story 1: Understand how the different tables merge together, and decide what data is necessary for this project
    *	(2 points) *** Story 2: Perform EDA, making sure the data is clean, makes sense, and there are no outliers, etc
    *	(2 points) *** Story 3: Create Final clean dataset that will be used to train the model
    *	(1 points) * Story 4: Document the code, paying special attention to any decision points
-	Epic 2: Create Recommendation System Model
    * (4 points) ** Story 1: Create a User-Based Collaborative Filtering Model
    * (4 points) ** Story 2: Create an Item Based Collaborative Filtering Model
    * (2 points) ** Story 3: Test how long each model takes to give users new recommendations - Decide which is better in terms of precision and run time
    * (2 points) * Story 4: Document the code, keeping the final model, and pay special attention to any decision points
    * (4 points) * Story 5: Create Unit tests
    * (1 point) * Story 6: Discuss with QA
    
 ## Icebox
 **Theme II:**
 
 Create the interactive user site – These epics will be built into stories later in the quarter, once we have the background knowledge of how to use Flask, AWS, etc.
 
*	Epic 1: Create environment and requirements needed for the project
*	Epic 2: Create the Flask/html/css code to run the user app
*	Epic 3: Store the final model/ratings matrix in S3
*	Epic 4: Store the book images in the RDS, and call images of the user’s recommendations from here
*	Epic 5: Check the Final Github Repo to ensure it meets all requirements

**Theme III:**

Create a longer lasting app that will allow users to store their recommendations and interact with these later

*	Epic 1: Store user recommendations
    *	Give each user a place to store their recommended books in a list
    *	Give users a place to display which books they have rated, and add comments about the book
*	Epic 2: Allow users to come back to the site and rate their recommendations
    *	Ask the user if they would like to mark their items as read
    *	Ask the user to rate these items that they have read
*	Epic 3: Update the model with these new ratings, or perhaps new books that are released.
