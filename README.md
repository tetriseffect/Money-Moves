My final project for CS50 is Money Moves - a budgeting / money management app. It allows users to enter items they have spent money on, and track them by category. Additionally, user's can view charts summarizing their spending by category or month.  The project uses the following languages/technologies : Python, Flask, Sqlite3, and Chart.js


The webapp has four pages:

Home Page - The main page displays a table showing every item the user has spent money on, along with the category, description, date, and cost. The user's total spending is calculated and displayed as well.

Add Item - The user can add an item to their budget. After selecting the category and cost, they can enter a short description. Submitting the form takes the user to the Home page, with their new item added.

Data - This page displays a pie chart, breaking down the user's costs by category. The chart is rendered using the Javascript library Chart.js. Below the graph, the page lists the user's total spending for each category since they started using the application.

History - The final page shows a bar graph that details the user's spending per month. This is also created using the library Chart.js.
