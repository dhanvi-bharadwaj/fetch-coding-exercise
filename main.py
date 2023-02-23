# importing neccessary libaries 
# to accept command line arguments
import sys 
# to efficiently handle large datasets in real world scenario
import pandas as pd

def balances(spending_points,filename):
    """
    Caulates the payer point balances for a user.

    Parameters:
    - spending_points: the total number of points the user wants to spend (integer)
    - filename: the name of the CSV file containing the transaction data (string)

    Returns:
    - a dictionary containing the new point balances for each payer (string -> integer)
      if the transaction is valid and there are enough points to spend
    - a dictionary containing an error message if the transaction is not valid

    The function reads the transaction data from the CSV file, sorts the transactions
    by their timestamp, and then calculates the total number of points for each payer.
    It then iterates over the transactions, spending the oldest points first, until the
    total number of spending points is reached or all points have been spent. If the
    total number of spending points is greater than the total number of points in the
    user's account, the function returns an error message.
    """

    # Converting the transaction data from the CSV file into dataframe
    df=pd.read_csv(filename) 
    # Converting the timestamp column to a datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Sorting the transactions by their timestamp in ascending order
    df=df.sort_values('timestamp', ascending=True).reset_index(drop=True)

    # Calculating the total number of points for each payer the user's account
    # Grouping the dataframe by payer and calculating total points available per payer
    points = df.groupby("payer",sort=False).sum().to_dict()['points']
    # Calculating total points available in user's account
    total_points = sum(points.values())
    total_copy = points.copy()

    # Iterating over the transactions to spend the oldest points first
    for i in range(len(df)):
        if spending_points>total_points:
            # Returning an error message if the total number of spending points is greater than
            # the total number of points in the user's account
            return {"Error" : f"You need {spending_points-total_points} more points in your account to make this purchase "\
             f"You currently have only {total_points} points, but you are trying to spend {spending_points} points"}
        elif spending_points>0:
            # Spending the points for each payer
            payer = (df.iloc[i])['payer']
            points_per_payer = (df.iloc[i])['points']

            if spending_points<points_per_payer:
                total_copy[payer] = total_copy[payer]-spending_points
                return total_copy
            total_copy[payer] -= points_per_payer
            spending_points -= points_per_payer
            if spending_points==0:
                return total_copy
        else: 
            # Returning an error message if the user is trying to spend more points than they have
            return {"Error": f"You are trying to spend {spending_points} points which is not possible. " \
                f"Please try again by spending more points"}
        
if __name__ == "__main__":
    # Getting the command line arguments
    arg1 = int(sys.argv[1])
    arg2 = sys.argv[2]
    # Calling the function with arguments
    result = balances(arg1, arg2)
    print(result)
            