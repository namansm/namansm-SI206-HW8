# Your name: Naman Mathur
# Your student id: 17661408
# Your email: namansm@umich.edu
# List who you have worked with on this homework: N/A

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    d = {}
    cur, conn = open_database(db)
    cur.execute("SELECT r.name, r.rating, c.category FROM restaurants r INNER JOIN categories c ON r.category_id = c.id")
    cat = cur.fetchall()
    cur.execute("SELECT b.building FROM restaurants r INNER JOIN buildings b ON r.building_id = b.id")
    build = cur.fetchall()

    for i in range(0,25):
        temp = {}
        temp["category"] = cat[i][2]
        temp["building"] = build[i][0]
        temp["rating"] = cat[i][1]
        d[cat[i][0]] = temp

    return d    

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    d = {}
    cur, conn = open_database(db)
    cur.execute("SELECT c.category, COUNT(category_id) FROM restaurants r INNER JOIN categories c ON r.category_id = c.id GROUP BY c.category")
    counts = cur.fetchall()

    for c in counts:
        d[c[0]] = c[1]
    
    d_sorted = dict(sorted(d.items(), key=lambda t : t[1], reverse=True))
    
    # plot
    rests = []
    nums = []
    for key, value in d_sorted.items():
        rests.append(key)
        nums.append(value)
    fig, ax = plt.subplots()
    ax.barh(rests, nums, align='center')
    #ax.set_yticks(, labels=people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of Restaurants')
    ax.set_xlabel('Type of Restaurant')
    ax.set_title('Number of Restaurants per Type')
     
    plt.savefig('rests_vs_nums.png')
    return d
    

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    l = []
    cur, conn = open_database(db)
    cur.execute("SELECT r.name, r.rating FROM restaurants r INNER JOIN buildings b ON r.building_id = b.id WHERE b.building=?", (building_num,))
    names = cur.fetchall()
    names = sorted(names, key=lambda t: t[1], reverse=True)
    for n in names:
        l.append(n[0])

    return l

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    # def test_get_highest_rating(self):
    #     highest_rating = get_highest_rating('South_U_Restaurants.db')
    #     self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
