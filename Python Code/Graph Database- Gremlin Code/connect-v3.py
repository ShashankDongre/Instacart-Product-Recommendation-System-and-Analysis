from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError
import sys
import traceback
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

_gremlin_cleanup_graph = "g.V().drop()"

_gremlin_insert_vertices = [
    "g.addV('product').property('id','Chocolate Sandwich Cookies').property('product_id', '1').property('product_name', 'Chocolate Sandwich Cookies').property('aisle_id', '61').property('department_id', '19').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'cookies cakes').property('aisle_id', '61').property('aisle', 'cookies cakes').property('pk', 'pk')",
    "g.addV('department').property('id', 'snacks').property('department_id', '19').property('department', 'snacks').property('aisle_id', '61').property('pk', 'pk')",
    
    "g.addV('product').property('id','All-Seasons Salt').property('product_id', '2').property('product_name', 'All-Seasons Salt').property('aisle_id', '104').property('department_id', '13').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'spices seasonings').property('aisle_id', '104').property('aisle', 'spices seasonings').property('pk', 'pk')",
    "g.addV('department').property('id', 'pantry').property('department_id', '13').property('department', 'pantry').property('aisle_id', 104).property('pk', 'pk')",
    
    "g.addV('product').property('id','Robust Golden Unsweetened Oolong Tea').property('product_id', '3').property('product_name', 'Robust Golden Unsweetened Oolong Tea').property('aisle_id', '94').property('department_id', '7').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'tea').property('aisle_id', '94').property('aisle', 'tea').property('pk', 'pk')",
    "g.addV('department').property('id', 'household').property('department_id', '7').property('department', 'household').property('aisle_id', '94').property('pk', 'pk')",
    
    "g.addV('product').property('id','Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce').property('product_id', '4').property('product_name', 'Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce').property('aisle_id', '38').property('department_id', '1').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'frozen meals').property('aisle_id', '38').property('aisle', 'frozen meals').property('pk', 'pk')",
    "g.addV('department').property('id', 'frozen').property('department_id', '1').property('department', 'frozen').property('aisle_id', '38').property('pk', 'pk')",
    
    "g.addV('product').property('id','Green Chile Anytime Sauce').property('product_id', '5').property('product_name', 'Green Chile Anytime Sauce').property('aisle_id', '5').property('department_id', '13').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'marinades meat preparation').property('aisle_id', '5').property('aisle', 'marinades meat preparation').property('pk', 'pk')",
    "g.addV('department').property('id', 'pantry').property('department_id', '13').property('department', 'pantry').property('aisle_id', '5').property('pk', 'pk')",
    
    #"g.addV('product').property('id','Dry Nose Oil').property('product_id', '6').property('product_name', 'Dry Nose Oil').property('aisle_id', '11').property('department_id', '11').property('pk', 'pk')",
    #"g.addV('aisle').property('id', 'cold flu allergy').property('aisle_id', '11').property('aisle', 'cold flu allergy').property('pk', 'pk')",
    #"g.addV('department').property('id', 'personal care').property('department_id', '11').property('department', 'personal care').property('aisle_id', '11').property('pk', 'pk')",
    
    "g.addV('product').property('id','Pure Coconut Water With Orange').property('product_id', '6').property('product_name', 'Pure Coconut Water With Orange').property('aisle_id', '98').property('department_id', '7').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'juice nectars').property('aisle_id', '98').property('aisle', 'juice nectars').property('pk', 'pk')",
    "g.addV('department').property('id', 'beverages').property('department_id', '7').property('department', 'beverages').property('aisle_id', '98').property('pk', 'pk')",
    
    "g.addV('product').property('id','Cut Russet Potatoes Steam N Mash').property('product_id', '7').property('product_name', 'Cut Russet Potatoes Steam N Mash').property('aisle_id', '116').property('department_id', '1').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'frozen produce').property('aisle_id', '116').property('aisle', 'frozen produce').property('pk', 'pk')",
    "g.addV('department').property('id', 'frozen').property('department_id', '1').property('department', 'frozen').property('aisle_id', '116').property('pk', 'pk')",
    
    "g.addV('product').property('id','Light Strawberry Blueberry Yogurt').property('product_id', '8').property('product_name', 'Light Strawberry Blueberry Yogurt').property('aisle_id', '120').property('department_id', '16').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'yogurt').property('aisle_id', '120').property('aisle', 'yogurt').property('pk', 'pk')",
    "g.addV('department').property('id', 'dairy eggs').property('department_id', '16').property('department', 'dairy eggs').property('aisle_id', '120').property('pk', 'pk')",
    
    
    "g.addV('product').property('id','Sparkling Orange Juice & Prickly Pear Beverage').property('product_id', '9').property('product_name', 'Sparkling Orange Juice & Prickly Pear Beverage').property('aisle_id', '115').property('department_id', '7').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'water seltzer sparkling water').property('aisle_id', '115').property('aisle', 'water seltzer sparkling water').property('pk', 'pk')",
    "g.addV('department').property('id', 'beverages').property('department_id', '7').property('department', 'beverages').property('aisle_id', '120').property('pk', 'pk')",
    
    "g.addV('product').property('id','Peach Mango Juice').property('product_id', '10').property('product_name', 'Peach Mango Juice').property('aisle_id', '31').property('department_id', '7').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'refrigerated').property('aisle_id', '31').property('aisle', 'refrigerated').property('pk', 'pk')",
    "g.addV('department').property('id', 'beverages').property('department_id', '7').property('department', 'beverages').property('aisle_id', '31').property('pk', 'pk')",
    
    "g.addV('product').property('id','Chocolate Fudge Layer Cake').property('product_id', '11').property('product_name', 'Chocolate Fudge Layer Cake').property('aisle_id', 119).property('department_id', 1).property('pk', 'pk')",
    "g.addV('aisle').property('id', 'frozen dessert').property('aisle_id', '119').property('aisle', 'frozen dessert').property('pk', 'pk')",
    "g.addV('department').property('id', 'frozen').property('department_id', '1').property('department', 'frozen').property('aisle_id', '119').property('pk', 'pk')",

    "g.addV('product').property('id','Saline Nasal Mist').property('product_id', '12').property('product_name', 'Saline Nasal Mist').property('aisle_id', '11').property('department_id', '11').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'cold flu allergy').property('aisle_id', '11').property('aisle', 'cold flu allergy').property('pk', 'pk')",
    "g.addV('department').property('id', 'personal care').property('department_id', '11').property('department', 'personal care').property('aisle_id', '11').property('pk', 'pk')",

    "g.addV('product').property('id','Fresh Scent Dishwasher Cleaner').property('product_id', '13').property('product_name', 'Fresh Scent Dishwasher Cleaner').property('aisle_id', '74').property('department_id', '17').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'dish detergents').property('aisle_id', '74').property('aisle', 'dish detergents').property('pk', 'pk')",
    "g.addV('department').property('id', 'household').property('department_id', '17').property('department', 'household').property('aisle_id', '74').property('pk', 'pk')",

    "g.addV('product').property('id','Overnight Diapers Size 6').property('product_id', '14').property('product_name', 'Saline Nasal Mist').property('aisle_id', '56').property('department_id', '18').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'diapers wipes').property('aisle_id', '56').property('aisle', 'diapers wipes').property('pk', 'pk')",
    "g.addV('department').property('id', 'babies').property('department_id', '18').property('department', 'babies').property('aisle_id', '56').property('pk', 'pk')",

    "g.addV('product').property('id','Mint Chocolate Flavored Syrup').property('product_id', '15').property('product_name', 'Mint Chocolate Flavored Syrup').property('aisle_id', '103').property('department_id', '19').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'ice cream toppings').property('aisle_id', '103').property('aisle', 'ice cream toppings').property('pk', 'pk')",
    "g.addV('department').property('id', 'snacks').property('department_id', '19').property('department', 'snacks').property('aisle_id', '103').property('pk', 'pk')",

    "g.addV('product').property('id','Rendered Duck Fat').property('product_id', '16').property('product_name', 'Rendered Duck Fat').property('aisle_id', '35').property('department_id', '12').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'poultry counter').property('aisle_id', '35').property('aisle', 'poultry counter').property('pk', 'pk')",
    "g.addV('department').property('id', 'meat seafood').property('department_id', '12').property('department', 'meat seafood').property('aisle_id', '35').property('pk', 'pk')",

    "g.addV('product').property('id','Pizza for One Suprema  Frozen Pizza').property('product_id', '17').property('product_name', 'Pizza for One Suprema  Frozen Pizza').property('aisle_id', '79').property('department_id', '1').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'frozen pizza').property('aisle_id', '79').property('aisle', 'frozen pizza').property('pk', 'pk')",
    "g.addV('department').property('id', 'frozen').property('department_id', '1').property('department', 'frozen').property('aisle_id', '79').property('pk', 'pk')",

    "g.addV('product').property('id','Gluten Free Quinoa Three Cheese & Mushroom Blend').property('product_id', '18').property('product_name', 'Gluten Free Quinoa Three Cheese & Mushroom Blend').property('aisle_id', '63').property('department_id', '9').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'grains rice dried goods').property('aisle_id', '63').property('aisle', 'grains rice dried goods').property('pk', 'pk')",
    "g.addV('department').property('id', 'dry goods pasta').property('department_id', '9').property('department', 'dry goods pasta').property('aisle_id', '63').property('pk', 'pk')",

    #"g.addV('product').property('id','Pomegranate Cranberry & Aloe Vera Enrich Drink').property('product_id', '20').property('product_name', 'Pomegranate Cranberry & Aloe Vera Enrich Drink').property('aisle_id', '98').property('department_id', '7').property('pk', 'pk')",
    #"g.addV('aisle').property('id', 'juice nectars').property('aisle_id', '98').property('aisle', 'juice nectars').property('pk', 'pk')",
    #"g.addV('department').property('id', 'beverages').property('department_id', '7').property('department', 'beverages').property('aisle_id', '98').property('pk', 'pk')",

    "g.addV('product').property('id','Small & Medium Dental Dog Treats').property('product_id', '19').property('product_name', 'Small & Medium Dental Dog Treats').property('aisle_id', '40').property('department_id', '11').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'dog food care').property('aisle_id', '40').property('aisle', 'dog food care').property('pk', 'pk')",
    "g.addV('department').property('id', 'pets').property('department_id', '8').property('department', 'pets').property('aisle_id', '40').property('pk', 'pk')",

    "g.addV('product').property('id','Fresh Breath Oral Rinse Mild Mint').property('product_id', '20').property('product_name', 'Fresh Breath Oral Rinse Mild Mint').property('aisle_id', '20').property('department_id', '11').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'oral hygiene').property('aisle_id', '20').property('aisle', 'oral hygiene').property('pk', 'pk')",
    "g.addV('department').property('id', 'personal care').property('department_id', '11').property('department', 'personal care').property('aisle_id', '20').property('pk', 'pk')",

    "g.addV('product').property('id','Organic Turkey Burgers').property('product_id', '21').property('product_name', 'Organic Turkey Burgers').property('aisle_id', '49').property('department_id', '12').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'packaged poultry').property('aisle_id', '49').property('aisle', 'packaged poultry').property('pk', 'pk')",
    "g.addV('department').property('id', 'meat seafood').property('department_id', '12').property('department', 'meat seafood').property('aisle_id', '49').property('pk', 'pk')",

    # "g.addV('product').property('id','Tri-Vi-Sol® Vitamins A-C-and D Supplement Drops for Infants').property('product_id', '24').property('product_name', 'Tri-Vi-Sol® Vitamins A-C-and D Supplement Drops for Infants').property('aisle_id', '47').property('department_id', '11').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'vitamins supplements').property('aisle_id', '47').property('aisle', 'vitamins supplements').property('pk', 'pk')",
    # "g.addV('department').property('id', 'personal care').property('department_id', '11').property('department', 'personal care').property('aisle_id', '47').property('pk', 'pk')",

    "g.addV('product').property('id','Salted Caramel Lean Protein & Fiber Bar').property('product_id', '22').property('product_name', 'Salted Caramel Lean Protein & Fiber Bar').property('aisle_id', '3').property('department_id', '19').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'energy granola bars').property('aisle_id', '3').property('aisle', 'energy granola bars').property('pk', 'pk')",
    "g.addV('department').property('id', 'snacks').property('department_id', '19').property('department', 'snacks').property('aisle_id', '3').property('pk', 'pk')",

    "g.addV('product').property('id','Fancy Feast Trout Feast Flaked Wet Cat Food').property('product_id', '23').property('product_name', 'Fancy Feast Trout Feast Flaked Wet Cat Food').property('aisle_id', '127').property('department_id', '11').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'cat food care').property('aisle_id', '127').property('aisle', 'cat food care').property('pk', 'pk')",
    "g.addV('department').property('id', 'pets').property('department_id', '11').property('department', 'pets').property('aisle_id', '127').property('pk', 'pk')",
    
    "g.addV('product').property('id','Complete Spring Water Foaming Antibacterial Hand Wash').property('product_id', '24').property('product_name', 'Complete Spring Water Foaming Antibacterial Hand Wash').property('aisle_id', '127').property('department_id', '11').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'body lotions soap').property('aisle_id', '127').property('aisle', 'body lotions soap').property('pk', 'pk')",
    "g.addV('department').property('id', 'personal care').property('department_id', '11').property('department', 'personal care').property('aisle_id', '127').property('pk', 'pk')",

    # "g.addV('product').property('id','Wheat Chex Cereal').property('product_id', '28').property('product_name', 'Wheat Chex Cereal').property('aisle_id', '121').property('department_id', '14').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'cereal').property('aisle_id', '121').property('aisle', 'cereal').property('pk', 'pk')",
    # "g.addV('department').property('id', 'breakfast').property('department_id', '14').property('department', 'breakfast').property('aisle_id', '121').property('pk', 'pk')",

    "g.addV('product').property('id','Fresh Cut Golden Sweet No Salt Added Whole Kernel Corn').property('product_id', '25').property('product_name', 'Fresh Cut Golden Sweet No Salt Added Whole Kernel Corn').property('aisle_id', '81').property('department_id', '15').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'canned jarred vegetables').property('aisle_id', '81').property('aisle', 'canned jarred vegetables').property('pk', 'pk')",
    "g.addV('department').property('id', 'canned goods').property('department_id', '15').property('department', 'canned goods').property('aisle_id', '81').property('pk', 'pk')",

    #"g.addV('product').property('id','Three Cheese Ziti, Marinara with Meatballs').property('product_id', '30').property('product_name', 'Three Cheese Ziti, Marinara with Meatballs').property('aisle_id', '38').property('department_id', '1').property('pk', 'pk')",
    #"g.addV('aisle').property('id', 'frozen meals').property('aisle_id', '38').property('aisle', 'frozen meals').property('pk', 'pk')",
    #"#g.addV('department').property('id', 'frozen').property('department_id', '1').property('department', 'frozen').property('aisle_id', '38').property('pk', 'pk')",

    "g.addV('product').property('id','White Pearl Onions').property('product_id', '26').property('product_name', 'White Pearl Onions').property('aisle_id', '123').property('department_id', '4').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'packaged vegetables fruits').property('aisle_id', '123').property('aisle', 'packaged vegetables fruits').property('pk', 'pk')",
    "g.addV('department').property('id', 'produce').property('department_id', '4').property('department', 'produce').property('aisle_id', '123').property('pk', 'pk')",

    "g.addV('product').property('id','Nacho Cheese White Bean Chips').property('product_id', '27').property('product_name', 'Nacho Cheese White Bean Chips').property('aisle_id', '107').property('department_id', '19').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'chips pretzels').property('aisle_id', '107').property('aisle', 'chips pretzels').property('pk', 'pk')",
    "g.addV('department').property('id', 'snacks').property('department_id', '19').property('department', 'snacks').property('aisle_id', '107').property('pk', 'pk')",

    "g.addV('product').property('id','Organic Spaghetti Style Pasta').property('product_id', '28').property('product_name', 'Organic Spaghetti Style Pasta').property('aisle_id', '131').property('department_id', '9').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'dry pasta').property('aisle_id', '131').property('aisle', 'dry pasta').property('pk', 'pk')",
    "g.addV('department').property('id', 'dry goods pasta').property('department_id', '9').property('department', 'dry goods pasta').property('aisle_id', '131').property('pk', 'pk')",

    "g.addV('product').property('id','Peanut Butter Cereal').property('product_id', '29').property('product_name', 'Peanut Butter Cereal').property('aisle_id', '121').property('department_id', '14').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'cereal').property('aisle_id', '121').property('aisle', 'cereal').property('pk', 'pk')",
    "g.addV('department').property('id', 'breakfast').property('department_id', '14').property('department', 'breakfast').property('aisle_id', '121').property('pk', 'pk')",

    # "g.addV('product').property('id','Italian Herb Porcini Mushrooms Chicken Sausage').property('product_id', '35').property('product_name', 'Italian Herb Porcini Mushrooms Chicken Sausage').property('aisle_id', '106').property('department_id', '12').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'hot dogs bacon sausage').property('aisle_id', '106').property('aisle', 'hot dogs bacon sausage').property('pk', 'pk')",
    # "g.addV('department').property('id', 'meat seafood').property('department_id', '12').property('department', 'meat seafood').property('aisle_id', '106').property('pk', 'pk')",

    #"g.addV('product').property('id','Traditional Lasagna with Meat Sauce Savory Italian Recipes').property('product_id', '36').property('product_name', 'Traditional Lasagna with Meat Sauce Savory Italian Recipes').property('aisle_id', '38').property('department_id', '1').property('pk', 'pk')",
    #"g.addV('aisle').property('id', 'frozen meals').property('aisle_id', '38').property('aisle', 'frozen meals').property('pk', 'pk')",
    #"g.addV('department').property('id', 'frozen').property('department_id', '1').property('department', 'frozen').property('aisle_id', '38').property('pk', 'pk')",

    "g.addV('product').property('id','Noodle Soup Mix With Chicken Broth').property('product_id', '30').property('product_name', 'Noodle Soup Mix With Chicken Broth').property('aisle_id', '69').property('department_id', '15').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'soup broth bouillon').property('aisle_id', '69').property('aisle', 'soup broth bouillon').property('pk', 'pk')",
    "g.addV('department').property('id', 'canned goods').property('department_id', '15').property('department', 'canned goods').property('aisle_id', '69').property('pk', 'pk')",

    # "g.addV('product').property('id','Ultra Antibacterial Dish Liquid').property('product_id', '38').property('product_name', 'Ultra Antibacterial Dish Liquid').property('aisle_id', '100').property('department_id', '21').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'missing').property('aisle_id', '100').property('aisle', 'missing').property('pk', 'pk')",
    # "g.addV('department').property('id', 'missing').property('department_id', '21').property('department', 'missing').property('aisle_id', '100').property('pk', 'pk')",

    "g.addV('product').property('id','Daily Tangerine Citrus Flavored Beverage').property('product_id', '31').property('product_name', 'Daily Tangerine Citrus Flavored Beverage').property('aisle_id', '64').property('department_id', '7').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'energy sports drinks').property('aisle_id', '64').property('aisle', 'energy sports drinks').property('pk', 'pk')",
    "g.addV('department').property('id', 'beverages').property('department_id', '7').property('department', 'beverages').property('aisle_id', '64').property('pk', 'pk')",

    "g.addV('product').property('id','Beef Hot Links Beef Smoked Sausage With Chile Peppers').property('product_id', '32').property('product_name', 'Beef Hot Links Beef Smoked Sausage With Chile Peppers').property('aisle_id', '106').property('department_id', '12').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'hot dogs bacon sausage').property('aisle_id', '106').property('aisle', 'hot dogs bacon sausage').property('pk', 'pk')",
    "g.addV('department').property('id', 'meat seafood').property('department_id', '12').property('department', 'meat seafood').property('aisle_id', '106').property('pk', 'pk')",

    "g.addV('product').property('id','Organic Sourdough Einkorn Crackers Rosemary').property('product_id', '33').property('product_name', 'Organic Sourdough Einkorn Crackers Rosemary').property('aisle_id', '78').property('department_id', '19').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'crackers').property('aisle_id', '78').property('aisle', 'crackers').property('pk', 'pk')",
    "g.addV('department').property('id', 'snacks').property('department_id', '19').property('department', 'snacks').property('aisle_id', '78').property('pk', 'pk')",

    "g.addV('product').property('id','Biotin 1000 mcg').property('product_id', '34').property('product_name', 'Biotin 1000 mcg').property('aisle_id', '47').property('department_id', '11').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'vitamins supplements').property('aisle_id', '47').property('aisle', 'vitamins supplements').property('pk', 'pk')",
    "g.addV('department').property('id', 'personal care').property('department_id', '11').property('department', 'personal care').property('aisle_id', '47').property('pk', 'pk')",

    # "g.addV('product').property('id','Organic Clementines').property('product_id', '43').property('product_name', 'Organic Clementines').property('aisle_id', '123').property('department_id', '4').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'packaged vegetables fruits').property('aisle_id', '123').property('aisle', 'packaged vegetables fruits').property('pk', 'pk')",
    # "g.addV('department').property('id', 'produce').property('department_id', '4').property('department', 'produce').property('aisle_id', '123').property('pk', 'pk')",

    # "g.addV('product').property('id','Sparkling Raspberry Seltzer').property('product_id', '44').property('product_name', 'Sparkling Raspberry Seltzer').property('aisle_id', '115').property('department_id', '7').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'water seltzer sparkling water').property('aisle_id', '115').property('aisle', 'water seltzer sparkling water').property('pk', 'pk')",
    # "g.addV('department').property('id', 'beverages').property('department_id', '7').property('department', 'beverages').property('aisle_id', '115').property('pk', 'pk')",
    
    "g.addV('product').property('id','European Cucumber').property('product_id', '35').property('product_name', 'European Cucumber').property('aisle_id', '83').property('department_id', '4').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'fresh vegetables').property('aisle_id', '83').property('aisle', 'fresh vegetables').property('pk', 'pk')",
    "g.addV('department').property('id', 'produce').property('department_id', '4').property('department', 'produce').property('aisle_id', '83').property('pk', 'pk')",

    "g.addV('product').property('id','Raisin Cinnamon Bagels 5 count').property('product_id', '36').property('product_name', 'Raisin Cinnamon Bagels 5 count').property('aisle_id', '58').property('department_id', '1').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'frozen breads doughs').property('aisle_id', '58').property('aisle', 'frozen breads doughs').property('pk', 'pk')",
    "g.addV('department').property('id', 'frozen').property('department_id', '1').property('department', 'frozen').property('aisle_id', '58').property('pk', 'pk')",

    "g.addV('product').property('id','Onion Flavor Organic Roasted Seaweed Snack').property('product_id', '37').property('product_name', 'Onion Flavor Organic Roasted Seaweed Snack').property('aisle_id', '66').property('department_id', '6').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'asian foods').property('aisle_id', '66').property('aisle', 'asian foods').property('pk', 'pk')",
    "g.addV('department').property('id', 'international').property('department_id', '6').property('department', 'international').property('aisle_id', '66').property('pk', 'pk')",

    # "g.addV('product').property('id','School Glue, Washable, No Run').property('product_id', '38').property('product_name', 'School Glue, Washable, No Run').property('aisle_id', '87').property('department_id', '17').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'more household').property('aisle_id', '87').property('aisle', 'more household').property('pk', 'pk')",
    # "g.addV('department').property('id', 'household').property('department_id', '17').property('department', 'household').property('aisle_id', '87').property('pk', 'pk')",

    # "g.addV('product').property('id','Vegetarian Grain Meat Sausages Italian - 4 CT').property('product_id', '39').property('product_name', 'Vegetarian Grain Meat Sausages Italian - 4 CT').property('aisle_id', '14').property('department_id', '20').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'tofu meat alternatives').property('aisle_id', '14').property('aisle', 'tofu meat alternatives').property('pk', 'pk')",
    # "g.addV('department').property('id', 'deli').property('department_id', '20').property('department', 'deli').property('aisle_id', '14').property('pk', 'pk')",

    "g.addV('product').property('id','Pumpkin Muffin Mix').property('product_id', '40').property('product_name', 'Pumpkin Muffin Mix').property('aisle_id', '105').property('department_id', '13').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'doughs gelatins bake mixes').property('aisle_id', '105').property('aisle', 'doughs gelatins bake mixes').property('pk', 'pk')",
    "g.addV('department').property('id', 'pantry').property('department_id', '13').property('department', 'pantry').property('aisle_id', '105').property('pk', 'pk')",

    # "g.addV('product').property('id','Raisin Cinnamon Bagels 5 count').property('product_id', '41').property('product_name', 'Raisin Cinnamon Bagels 5 count').property('aisle_id', '58').property('department_id', '1').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'frozen breads doughs').property('aisle_id', '58').property('aisle', 'frozen breads doughs').property('pk', 'pk')",
    # "g.addV('department').property('id', 'frozen').property('department_id', '1').property('department', 'frozen').property('aisle_id', '58').property('pk', 'pk')",

    # "g.addV('product').property('id','Onion Flavor Organic Roasted Seaweed Snack').property('product_id', '42').property('product_name', 'Onion Flavor Organic Roasted Seaweed Snack').property('aisle_id', '66').property('department_id', '6').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'asian foods').property('aisle_id', '66').property('aisle', 'asian foods').property('pk', 'pk')",
    # "g.addV('department').property('id', 'international').property('department_id', '6').property('department', 'international').property('aisle_id', '66').property('pk', 'pk')",

    "g.addV('product').property('id','School Glue, Washable, No Run').property('product_id', '43').property('product_name', 'School Glue, Washable, No Run').property('aisle_id', '87').property('department_id', '17').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'more household').property('aisle_id', '87').property('aisle', 'more household').property('pk', 'pk')",
    "g.addV('department').property('id', 'household').property('department_id', '17').property('department', 'household').property('aisle_id', '87').property('pk', 'pk')",

    "g.addV('product').property('id','Vegetarian Grain Meat Sausages Italian - 4 CT').property('product_id', '44').property('product_name', 'Vegetarian Grain Meat Sausages Italian - 4 CT').property('aisle_id', '14').property('department_id', '20').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'tofu meat alternatives').property('aisle_id', '14').property('aisle', 'tofu meat alternatives').property('pk', 'pk')",
    "g.addV('department').property('id', 'deli').property('department_id', '20').property('department', 'deli').property('aisle_id', '14').property('pk', 'pk')",

    # "g.addV('product').property('id','Pumpkin Muffin Mix').property('product_id', '45').property('product_name', 'Pumpkin Muffin Mix').property('aisle_id', '105').property('department_id', '13').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'doughs gelatins bake mixes').property('aisle_id', '105').property('aisle', 'doughs gelatins bake mixes').property('pk', 'pk')",
    # "g.addV('department').property('id', 'pantry').property('department_id', '13').property('department', 'pantry').property('aisle_id', '105').property('pk', 'pk')",

    "g.addV('product').property('id','Sa Extra Hold Mousse Hair Styling').property('product_id', '46').property('product_name', 'Sa Extra Hold Mousse Hair Styling').property('aisle_id', '22').property('department_id', '11').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'hair care').property('aisle_id', '22').property('aisle', 'hair care').property('pk', 'pk')",
    "g.addV('department').property('id', 'personal care').property('department_id', '11').property('department', 'personal care').property('aisle_id', '22').property('pk', 'pk')",

    "g.addV('product').property('id','Mirabelle Brut Rose').property('product_id', '47').property('product_name', 'Mirabelle Brut Rose').property('aisle_id', '134').property('department_id', '5').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'specialty wines champagnes').property('aisle_id', '134').property('aisle', 'specialty wines champagnes').property('pk', 'pk')",
    "g.addV('department').property('id', 'alcohol').property('department_id', '5').property('department', 'alcohol').property('aisle_id', '134').property('pk', 'pk')",

    "g.addV('product').property('id','Healthy Pop Butter Popcorn').property('product_id', '48').property('product_name', 'Healthy Pop Butter Popcorn').property('aisle_id', '23').property('department_id', '19').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'popcorn jerky').property('aisle_id', '23').property('aisle', 'popcorn jerky').property('pk', 'pk')",
    "g.addV('department').property('id', 'snacks').property('department_id', '19 ').property('department', 'snacks').property('aisle_id', '23').property('pk', 'pk')",

    "g.addV('product').property('id','Flat Toothpicks').property('product_id', '49').property('product_name', 'Flat Toothpicks').property('aisle_id', '111').property('department_id', '17').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'plates bowls cups flatware').property('aisle_id', '111').property('aisle', 'plates bowls cups flatware').property('pk', 'pk')",
    "g.addV('department').property('id', 'household').property('department_id', '17').property('department', 'household').property('aisle_id', '111').property('pk', 'pk')",

    "g.addV('product').property('id','Whole Wheat Tortillas').property('product_id', '50').property('product_name', 'Whole Wheat Tortillas').property('aisle_id', '128').property('department_id', '3').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'tortillas flat bread').property('aisle_id', '105').property('aisle', 'tortillas flat bread').property('pk', 'pk')",
    "g.addV('department').property('id', 'bakery').property('department_id', '3').property('department', 'bakery').property('aisle_id', '128').property('pk', 'pk')",

    "g.addV('product').property('id','Medium Taqueria Style Chipotle Salsa').property('product_id', '51').property('product_name', 'Medium Taqueria Style Chipotle Salsa').property('aisle_id', '50').property('department_id', '19').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'fruit vegetable snacks').property('aisle_id', '50').property('aisle', 'fruit vegetable snacks').property('pk', 'pk')",
    "g.addV('department').property('id', 'snacks').property('department_id', '1').property('department', 'snacks').property('aisle_id', '50').property('pk', 'pk')",

    "g.addV('product').property('id','Cheesy Creations Roasted Garlic Parmesan Sauce').property('product_id', '52').property('product_name', 'Cheesy Creations Roasted Garlic Parmesan Sauce').property('aisle_id', '9').property('department_id', '9').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'pasta sauce').property('aisle_id', '9').property('aisle', 'pasta sauce').property('pk', 'pk')",
    "g.addV('department').property('id', 'dry goods pasta').property('department_id', '9').property('department', 'dry goods pasta').property('aisle_id', '9').property('pk', 'pk')",

    "g.addV('product').property('id','Premium Deli Oven Roasted Turkey Breast').property('product_id', '53').property('product_name', 'Premium Deli Oven Roasted Turkey Breast').property('aisle_id', '96').property('department_id', '20').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'lunch meat').property('aisle_id', '96').property('aisle', 'lunch meat').property('pk', 'pk')",
    "g.addV('department').property('id', 'deli').property('department_id', '20').property('department', 'deli').property('aisle_id', '96').property('pk', 'pk')",

    "g.addV('product').property('id','Banana & Sweet Potato Organic Teething Wafers').property('product_id', '54').property('product_name', 'Banana & Sweet Potato Organic Teething Wafers').property('aisle_id', '92').property('department_id', '18').property('pk', 'pk')",
    "g.addV('aisle').property('id', 'baby food formula').property('aisle_id', '92').property('aisle', 'baby food formula').property('pk', 'pk')",
    "g.addV('department').property('id', 'babies').property('department_id', '18').property('department', 'babies').property('aisle_id', '92').property('pk', 'pk')",

    # "g.addV('product').property('id','Organic Red Wine & Olive Oil Dressing Organic').property('product_id', '55').property('product_name', 'Organic Red Wine & Olive Oil Dressing Organic').property('aisle_id', '89').property('department_id', '13').property('pk', 'pk')",
    # "g.addV('aisle').property('id', 'salad dressing toppings').property('aisle_id', '89').property('aisle', 'salad dressing toppings').property('pk', 'pk')",
    # "g.addV('department').property('id', 'pantry').property('department_id', '13').property('department', 'pantry').property('aisle_id', '105').property('pk', 'pk')"
]

_gremlin_insert_edges = [
    "g.V('Chocolate Sandwich Cookies').addE('belongs to').to(g.V('cookies cakes'))",
"g.V('snacks').addE('contains').to(g.V('cookies cakes'))",
"g.V('snacks').addE('has').to(g.V('Chocolate Sandwich Cookies'))",

"g.V('All-Seasons Salt').addE('belongs to').to(g.V('spices seasonings'))",
"g.V('pantry').addE('contains').to(g.V('spices seasonings'))",
"g.V('pantry').addE('has').to(g.V('All-Seasons Salt'))",

"g.V('Robust Golden Unsweetened Oolong Teas').addE('belongs to').to(g.V('tea'))",
"g.V('household').addE('contains').to(g.V('tea'))",
"g.V('household').addE('has').to(g.V('Robust Golden Unsweetened Oolong Tea'))",

"g.V('Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce').addE('belongs to').to(g.V('frozen meals'))",
"g.V('frozen').addE('contains').to(g.V('frozen meals'))",
"g.V('frozen').addE('has').to(g.V('Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce'))",

"g.V('Green Chile Anytime Sauce').addE('belongs to').to(g.V('marinades meat preparation'))",
"g.V('pantry').addE('contains').to(g.V('marinades meat preparation'))",
"g.V('pantry').addE('has').to(g.V('Green Chile Anytime Sauce'))",

#"g.V('Dry Nose Oil').addE('belongs to').to(g.V('cold flu allergy'))",
#"g.V('personal care').addE('contains').to(g.V('cold flu allergy'))",
#"g.V('personal care').addE('has').to(g.V('Dry Nose Oil'))",

"g.V('Pure Coconut Water With Orange').addE('belongs to').to(g.V('juice nectars'))",
"g.V('beverages').addE('contains').to(g.V('juice nectars'))",
"g.V('beverages').addE('has').to(g.V('Pure Coconut Water With Orange'))",

"g.V('Cut Russet Potatoes Steam N Mash').addE('belongs to').to(g.V('frozen produce'))",
"g.V('frozen').addE('contains').to(g.V('frozen produce'))",
"g.V('frozen').addE('has').to(g.V('Cut Russet Potatoes Steam N Mash'))",

"g.V('Light Strawberry Blueberry Yogurt').addE('belongs to').to(g.V('yogurt'))",
"g.V('dairy eggs').addE('contains').to(g.V('yogurt'))",
"g.V('dairy eggs').addE('has').to(g.V('Light Strawberry Blueberry Yogurt'))",

"g.V('Sparkling Orange Juice & Prickly Pear Beverage').addE('belongs to').to(g.V('water seltzer sparkling water'))",
"g.V('beverages').addE('contains').to(g.V('water seltzer sparkling water'))",
"g.V('beverages').addE('has').to(g.V('Sparkling Orange Juice & Prickly Pear Beverage'))",

"g.V('Peach Mango Juice').addE('belongs to').to(g.V('refrigerated'))",
"g.V('beverages').addE('contains').to(g.V('refrigerated'))",
"g.V('beverages').addE('has').to(g.V('Peach Mango Juice'))",

"g.V('Chocolate Fudge Layer Cake').addE('belongs to').to(g.V('frozen dessert'))",
"g.V('frozen').addE('contains').to(g.V('frozen dessert'))",
"g.V('frozen').addE('has').to(g.V('Chocolate Fudge Layer Cake'))",

"g.V('Saline Nasal Mist').addE('belongs to').to(g.V('cold flu allergy'))",
"g.V('personal care').addE('contains').to(g.V('cold flu allergy'))",
"g.V('personal care').addE('has').to(g.V('Saline Nasal Mist'))",

"g.V('Fresh Scent Dishwasher Cleaner').addE('belongs to').to(g.V('dish detergents'))",
"g.V('household').addE('contains').to(g.V('dish detergents'))",
"g.V('household').addE('has').to(g.V('Fresh Scent Dishwasher Cleaner'))",

"g.V('Overnight Diapers Size 6').addE('belongs to').to(g.V('diapers wipes'))",
"g.V('babies').addE('contains').to(g.V('diapers wipes'))",
"g.V('babies').addE('has').to(g.V('Overnight Diapers Size 6'))",

"g.V('Mint Chocolate Flavored Syrup').addE('belongs to').to(g.V('ice cream toppings'))",
"g.V('snacks').addE('contains').to(g.V('ice cream toppings'))",
"g.V('snacks').addE('has').to(g.V('Mint Chocolate Flavored Syrup'))",

"g.V('Rendered Duck Fat').addE('belongs to').to(g.V('poultry counter'))",
"g.V('meat seafood').addE('contains').to(g.V('poultry counter'))",
"g.V('meat seafood').addE('has').to(g.V('Rendered Duck Fat'))",

"g.V('Pizza for One Suprema  Frozen Pizza').addE('belongs to').to(g.V('frozen pizza'))",
"g.V('frozen').addE('contains').to(g.V('frozen pizza'))",
"g.V('frozen').addE('has').to(g.V('Pizza for One Suprema  Frozen Pizza'))",

"g.V('Gluten Free Quinoa Three Cheese & Mushroom Blend').addE('belongs to').to(g.V('grains rice dried goods'))",
"g.V('dry goods pasta').addE('contains').to(g.V('grains rice dried goods'))",
"g.V('dry goods pasta').addE('has').to(g.V('Gluten Free Quinoa Three Cheese & Mushroom Blend'))",

#"g.V('Pomegranate Cranberry & Aloe Vera Enrich Drink'').addE('belongs to').to(g.V('juice nectars'))",
#"g.V('beverages').addE('contains').to(g.V('juice nectars'))",
#"g.V('beverages').addE('has').to(g.V('Pomegranate Cranberry & Aloe Vera Enrich Drink''))",

"g.V('Small & Medium Dental Dog Treats').addE('belongs to').to(g.V('dog food care'))",
"g.V('pets').addE('contains').to(g.V('dog food care'))",
"g.V('pets').addE('has').to(g.V('Small & Medium Dental Dog Treats'))",

"g.V('Fresh Breath Oral Rinse Mild Mint').addE('belongs to').to(g.V('oral hygiene'))",
"g.V('personal care').addE('contains').to(g.V('oral hygiene'))",
"g.V('personal care').addE('has').to(g.V('Fresh Breath Oral Rinse Mild Mint'))",

"g.V('Organic Turkey Burgers').addE('belongs to').to(g.V('packaged poultry'))",
"g.V('meat seafood').addE('contains').to(g.V('packaged poultry'))",
"g.V('meat seafood').addE('has').to(g.V('Organic Turkey Burgers'))",

# "g.V('Tri-Vi-Sol® Vitamins A-C-and D Supplement Drops for Infants').addE('belongs to').to(g.V('vitamins supplements'))",
# "g.V('personal care').addE('contains').to(g.V('vitamins supplements'))",
# "g.V('personal care').addE('has').to(g.V('Tri-Vi-Sol® Vitamins A-C-and D Supplement Drops for Infants'))",

"g.V('Salted Caramel Lean Protein & Fiber Bar').addE('belongs to').to(g.V('energy granola bars'))",
"g.V('snacks').addE('contains').to(g.V('energy granola bars'))",
"g.V('snacks').addE('has').to(g.V('Salted Caramel Lean Protein & Fiber Bar'))",

"g.V('Fancy Feast Trout Feast Flaked Wet Cat Food').addE('belongs to').to(g.V('ccat food care'))",
"g.V('pets').addE('contains').to(g.V('cat food care'))",
"g.V('pets').addE('has').to(g.V('Fancy Feast Trout Feast Flaked Wet Cat Food'))",

"g.V('Complete Spring Water Foaming Antibacterial Hand Wash').addE('belongs to').to(g.V('body lotions soap'))",
"g.V('personal care').addE('contains').to(g.V('body lotions soap'))",
"g.V('personal care').addE('has').to(g.V('Complete Spring Water Foaming Antibacterial Hand Wash'))",

# "g.V('Wheat Chex Cereal').addE('belongs to').to(g.V('cereal'))",
# "g.V('breakfast').addE('contains').to(g.V('cereal'))",
# "g.V('breakfast').addE('has').to(g.V('Wheat Chex Cereal'))",

"g.V('Fresh Cut Golden Sweet No Salt Added Whole Kernel Corn').addE('belongs to').to(g.V('canned jarred vegetables'))",
"g.V('canned goods').addE('contains').to(g.V('canned jarred vegetables'))",
"g.V('canned goods').addE('has').to(g.V('Fresh Cut Golden Sweet No Salt Added Whole Kernel Corn'))",

#"g.V('Three Cheese Ziti, Marinara with Meatballs').addE('belongs to').to(g.V('frozen meals'))",
#"g.V('frozen').addE('contains').to(g.V('frozen meals'))",
#"g.V('frozen').addE('has').to(g.V('Three Cheese Ziti, Marinara with Meatballs'))",

"g.V('White Pearl Onions').addE('belongs to').to(g.V('packaged vegetables fruits'))",
"g.V('produce').addE('contains').to(g.V('packaged vegetables fruits'))",
"g.V('produce').addE('has').to(g.V('White Pearl Onions'))",

"g.V('Nacho Cheese White Bean Chips').addE('belongs to').to(g.V('chips pretzels'))",
"g.V('snacks').addE('contains').to(g.V('chips pretzels'))",
"g.V('snacks').addE('has').to(g.V('Nacho Cheese White Bean Chips'))",

"g.V('Organic Spaghetti Style Pasta').addE('belongs to').to(g.V('dry pasta'))",
"g.V('dry goods pasta').addE('contains').to(g.V('dry pasta'))",
"g.V('dry goods pasta').addE('has').to(g.V('Organic Spaghetti Style Pasta'))",

"g.V('Cut Russet Potatoes Steam N Mash').addE('belongs to').to(g.V('frozen produce'))",
"g.V('frozen').addE('contains').to(g.V('frozen produce'))",
"g.V('frozen').addE('has').to(g.V('Cut Russet Potatoes Steam N Mash'))",

"g.V('Peanut Butter Cereal').addE('belongs to').to(g.V('cereal'))",
"g.V('breakfast').addE('contains').to(g.V('cereal'))",
"g.V('breakfast').addE('has').to(g.V('Peanut Butter Cereal'))",

# "g.V('Italian Herb Porcini Mushrooms Chicken Sausage').addE('belongs to').to(g.V('hot dogs bacon sausage'))",
# "g.V('meat seafood').addE('contains').to(g.V('hot dogs bacon sausage'))",
# "g.V('meat seafood').addE('has').to(g.V('Italian Herb Porcini Mushrooms Chicken Sausage'))",

# "g.V('Traditional Lasagna with Meat Sauce Savory Italian Recipes').addE('belongs to').to(g.V('frozen meals'))",
# "g.V('frozen').addE('contains').to(g.V('frozen meals'))",
# "g.V('frozen').addE('has').to(g.V('Traditional Lasagna with Meat Sauce Savory Italian Recipes'))",

"g.V('Noodle Soup Mix With Chicken Broth').addE('belongs to').to(g.V('soup broth bouillon'))",
"g.V('canned goods').addE('contains').to(g.V('soup broth bouillon'))",
"g.V('canned goods').addE('has').to(g.V('Noodle Soup Mix With Chicken Broth'))",

"g.V('Saline Nasal Mist').addE('belongs to').to(g.V('cold flu allergy'))",
"g.V('personal care').addE('contains').to(g.V('cold flu allergy'))",
"g.V('personal care').addE('has').to(g.V('Saline Nasal Mist'))",

# "g.V('Ultra Antibacterial Dish Liquid').addE('belongs to').to(g.V('missing'))",
# "g.V('missing').addE('contains').to(g.V('missing'))",
# "g.V('missing').addE('has').to(g.V('Ultra Antibacterial Dish Liquid'))",

"g.V('Daily Tangerine Citrus Flavored Beverage').addE('belongs to').to(g.V('energy sports drinks'))",
"g.V('beverages').addE('contains').to(g.V('energy sports drinks'))",
"g.V('beverages').addE('has').to(g.V('Daily Tangerine Citrus Flavored Beverage'))",

"g.V('Beef Hot Links Beef Smoked Sausage With Chile Peppers').addE('belongs to').to(g.V('hot dogs bacon sausage'))",
"g.V('meat seafood').addE('contains').to(g.V('hot dogs bacon sausage'))",
"g.V('meat seafood').addE('has').to(g.V('Beef Hot Links Beef Smoked Sausage With Chile Peppers'))",

"g.V('Organic Sourdough Einkorn Crackers Rosemary').addE('belongs to').to(g.V('crackers'))",
"g.V('snacks').addE('contains').to(g.V('crackers'))",
"g.V('snacks').addE('has').to(g.V('Organic Sourdough Einkorn Crackers Rosemary'))",

"g.V('Biotin 1000 mcg').addE('belongs to').to(g.V('vitamins supplements'))",
"g.V('personal care').addE('contains').to(g.V('vitamins supplements'))",
"g.V('personal care').addE('has').to(g.V('Biotin 1000 mcg'))",

# "g.V('Organic Clementines').addE('belongs to').to(g.V('packaged vegetables fruits'))",
# "g.V('produce').addE('contains').to(g.V('packaged vegetables fruits'))",
# "g.V('produce').addE('has').to(g.V('Organic Clementines'))",

# "g.V('Sparkling Raspberry Seltzer').addE('belongs to').to(g.V('water seltzer sparkling water'))",
# "g.V('beverages').addE('contains').to(g.V('water seltzer sparkling water'))",
# "g.V('beverages').addE('has').to(g.V('Sparkling Raspberry Seltzer'))",

"g.V('European Cucumber').addE('belongs to').to(g.V('fresh vegetables'))",
"g.V('produce').addE('contains').to(g.V('fresh vegetables'))",
"g.V('produce').addE('has').to(g.V('European Cucumber'))",

"g.V('Raisin Cinnamon Bagels 5 count').addE('belongs to').to(g.V('frozen breads doughs'))",
"g.V('frozen').addE('contains').to(g.V('frozen breads doughs'))",
"g.V('frozen').addE('has').to(g.V('Raisin Cinnamon Bagels 5 count'))",

"g.V('School Glue, Washable, No Run').addE('belongs to').to(g.V('more household'))",
"g.V('household').addE('contains').to(g.V('more household'))",
"g.V('household').addE('has').to(g.V('School Glue, Washable, No Run'))",

"g.V('Vegetarian Grain Meat Sausages Italian - 4 CT').addE('belongs to').to(g.V('tofu meat alternatives'))",
"g.V('deli').addE('contains').to(g.V('tofu meat alternatives'))",
"g.V('deli').addE('has').to(g.V('Vegetarian Grain Meat Sausages Italian - 4 CT'))",

"g.V('Pumpkin Muffin Mix').addE('belongs to').to(g.V('doughs gelatins bake mixes'))",
"g.V('pantry').addE('contains').to(g.V('doughs gelatins bake mixes'))",
"g.V('pantry').addE('has').to(g.V('Pumpkin Muffin Mix'))",

"g.V('Sa Extra Hold Mousse Hair Styling').addE('belongs to').to(g.V('hair care'))",
"g.V('personal care').addE('contains').to(g.V('hair care'))",
"g.V('personal care').addE('has').to(g.V('Sa Extra Hold Mousse Hair Styling'))",

"g.V('Mirabelle Brut Ros').addE('belongs to').to(g.V('specialty wines champagnes'))",
"g.V('alcohol').addE('contains').to(g.V('specialty wines champagnes'))",
"g.V('alcohol').addE('has').to(g.V('Mirabelle Brut Ros'))",

"g.V('Healthy Pop Butter Popcorn').addE('belongs to').to(g.V('popcorn jerky'))",
"g.V('snacks').addE('contains').to(g.V('popcorn jerky'))",
"g.V('snacks').addE('has').to(g.V('Healthy Pop Butter Popcorn'))",

"g.V('Flat Toothpicks').addE('belongs to').to(g.V('plates bowls cups flatware'))",
"g.V('household').addE('contains').to(g.V('plates bowls cups flatware'))",
"g.V('household').addE('has').to(g.V('Flat Toothpicks'))",

"g.V('Whole Wheat Tortillas').addE('belongs to').to(g.V('tortillas flat bread'))",
"g.V('bakery').addE('contains').to(g.V('tortillas flat bread'))",
"g.V('bakery').addE('has').to(g.V('Whole Wheat Tortillas'))",

"g.V('Medium Taqueria Style Chipotle Salsa').addE('belongs to').to(g.V('fruit vegetable snacks'))",
"g.V('snacks').addE('contains').to(g.V('fruit vegetable snacks'))",
"g.V('snacks').addE('has').to(g.V('Medium Taqueria Style Chipotle Salsa'))",

"g.V('Cheesy Creations Roasted Garlic Parmesan Sauce').addE('belongs to').to(g.V('pasta sauce'))",
"g.V('dry goods pasta').addE('contains').to(g.V('pasta sauce'))",
"g.V('dry goods pasta').addE('has').to(g.V('Cheesy Creations Roasted Garlic Parmesan Sauce'))",

"g.V('Premium Deli Oven Roasted Turkey Breast').addE('belongs to').to(g.V('lunch meat'))",
"g.V('deli').addE('contains').to(g.V('lunch meat'))",
"g.V('deli').addE('has').to(g.V('Premium Deli Oven Roasted Turkey Breast'))",

"g.V('Banana & Sweet Potato Organic Teething Wafers').addE('belongs to').to(g.V('baby food formula'))",
"g.V('babies').addE('contains').to(g.V('baby food formula'))",
"g.V('babies').addE('has').to(g.V('Banana & Sweet Potato Organic Teething Wafers'))",

# "g.V('Organic Red Wine & Olive Oil Dressing Organic').addE('belongs to').to(g.V('salad dressing toppings'))",
# "g.V('pantry').addE('contains').to(g.V('salad dressing toppings'))",
# "g.V('pantry').addE('has').to(g.V('Organic Red Wine & Olive Oil Dressing Organic'))"


]

#_gremlin_update_vertices = [
#    "g.V('thomas').property('age', 45)"
#]

_gremlin_count_vertices = "g.V().count()"

#_gremlin_traversals = {
 #   "Get all persons older than 40": "g.V().hasLabel('person').has('age', gt(40)).values('firstName', 'age')",
#    "Get all persons and their first name": "g.V().hasLabel('person').values('firstName')",
  #  "Get all persons sorted by first name": "g.V().hasLabel('person').order().by('firstName', incr).values('firstName')",
   # "Get all persons that Thomas knows": "g.V('thomas').out('knows').hasLabel('person').values('firstName')",
    #"People known by those who Thomas knows": "g.V('thomas').out('knows').hasLabel('person').out('knows').hasLabel('person').values('firstName')",
    #"Get the path from Thomas to Robin": "g.V('thomas').repeat(out()).until(has('id', 'robin')).path().by('firstName')"
#}

#_gremlin_drop_operations = {
 #   "Drop Edge - Thomas no longer knows Mary": "g.V('thomas').outE('knows').where(inV().has('id', 'mary')).drop()",
  #  "Drop Vertex - Drop Thomas": "g.V('thomas').drop()"
#}

def print_status_attributes(result):
    # This logs the status attributes returned for successful requests.
    # See list of available response status attributes (headers) that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    #
    # These responses includes total request units charged and total server latency time.
    # 
    # IMPORTANT: Make sure to consume ALL results returend by cliient tothe final status attributes
    # for a request. Gremlin result are stream as a sequence of partial response messages
    # where the last response contents the complete status attributes set.
    #
    # This can be 
    print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))

def cleanup_graph(client):
    print("\n> {0}".format(
        _gremlin_cleanup_graph))
    callback = client.submitAsync(_gremlin_cleanup_graph)
    if callback.result() is not None:
        callback.result().all().result() 
    print("\n")
    print_status_attributes(callback.result())
    print("\n")


def insert_vertices(client):
    for query in _gremlin_insert_vertices:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this vertex:\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(query))
        print("\n")
        print_status_attributes(callback.result())
        print("\n")

    print("\n")


def insert_edges(client):
    for query in _gremlin_insert_edges:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this edge:\n\t{0}\n".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))
        print_status_attributes(callback.result())
        print("\n")

    print("\n")


#def update_vertices(client):
#    for query in _gremlin_update_vertices:
#        print("\n> {0}\n".format(query))
#        callback = client.submitAsync(query)
#        if callback.result() is not None:
#            print("\tUpdated this vertex:\n\t{0}\n".format(
#                callback.result().all().result()))
#        else:
#            print("Something went wrong with this query:\n\t{0}".format(query))
#
#        print_status_attributes(callback.result())
#        print("\n")

#    print("\n")


def count_vertices(client):
    print("\n> {0}".format(
        _gremlin_count_vertices))
    callback = client.submitAsync(_gremlin_count_vertices)
    if callback.result() is not None:
        print("\tCount of vertices: {0}".format(callback.result().all().result()))
    else:
        print("Something went wrong with this query: {0}".format(
            _gremlin_count_vertices))

    print("\n")
    print_status_attributes(callback.result())
    print("\n")


#def execute_traversals(client):
#    for key in _gremlin_traversals:
#        print("{0}:".format(key))
#        print("> {0}\n".format(
 #           _gremlin_traversals[key]))
#        callback = client.submitAsync(_gremlin_traversals[key])
#        for result in callback.result():
#            print("\t{0}".format(str(result)))
        
#        print("\n")
 #       print_status_attributes(callback.result())
#        print("\n")


#def execute_drop_operations(client):
#    for key in _gremlin_drop_operations:
#        print("{0}:".format(key))
 #       print("\n> {0}".format(
  #          _gremlin_drop_operations[key]))
   #     callback = client.submitAsync(_gremlin_drop_operations[key])
    #    for result in callback.result():
     #       print(result)
      #  print_status_attributes(callback.result())
       # print("\n")


try:
    client = client.Client('wss://project10-gremlin.gremlin.cosmos.azure.com:443/', 'g',
                           username="/dbs/project10/colls/Graph1",
                           password="UMAOPX34DBNHrFS5TpWG1WQmsnXQxmov7phCS51EoDchEJV7p97ti0ELydH2dfWx5Cfj0i90xyypACDbu9nLJg==",
                           message_serializer=serializer.GraphSONSerializersV2d0()
                           )

    print("Welcome to Azure Cosmos DB + Gremlin on Python!")

    # Drop the entire Graph
    input("We're about to drop whatever graph is on the server. Press any key to continue...")
    cleanup_graph(client)

    # Insert all vertices
    input("Let's insert some vertices into the graph. Press any key to continue...")
    insert_vertices(client)

    # Create edges between vertices
    input("Now, let's add some edges between the vertices. Press any key to continue...")
    insert_edges(client)

    # Update a vertex
    #input("Ah, sorry. I made a mistake. Let's change the age of this vertex. Press any key to continue...")
    #update_vertices(client)

    # Count all vertices
    input("Okay. Let's count how many vertices we have. Press any key to continue...")
    count_vertices(client)

    # Execute traversals and get results
    #input("Cool! Let's run some traversals on our graph. Press any key to continue...")
    #execute_traversals(client)

    # Drop a few vertices and edges
    #input("So, life happens and now we will make some changes to the graph. Press any key to continue...")
    #execute_drop_operations(client)

    # Count all vertices again
    input("How many vertices do we have left? Press any key to continue...")
    count_vertices(client)

except GremlinServerError as e:
    print('Code: {0}, Attributes: {1}'.format(e.status_code, e.status_attributes))

    # GremlinServerError.status_code returns the Gremlin protocol status code
    # These are broad status codes which can cover various scenaios, so for more specific
    # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
    # 
    # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
    # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
    #
    # See also list of available response status attributes that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    cosmos_status_code = e.status_attributes["x-ms-status-code"]
    if cosmos_status_code == 409:
        print('Conflict error!')
    elif cosmos_status_code == 412:
        print('Precondition error!')
    elif cosmos_status_code == 429:
        print('Throttling error!');
    elif cosmos_status_code == 1009:
        print('Request timeout error!')
    else:
        print("Default error handling")

    traceback.print_exc(file=sys.stdout) 
    sys.exit(1)

print("\nAnd that's all! Sample complete")
input("Press Enter to continue...")
