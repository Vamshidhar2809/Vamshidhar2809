import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ice_cream_parlor.db')
    return conn

def add_flavor(conn, name, season=None, description=None):
    c = conn.cursor()
    c.execute("INSERT INTO Flavors (name, season, description) VALUES (?,?,?)", (name, season, description))
    conn.commit()

def add_ingredient(conn, name, flavor_id):
    c = conn.cursor()
    c.execute("INSERT INTO Ingredients (name, flavor_id) VALUES (?,?)", (name, flavor_id))
    conn.commit()

def add_allergen(conn, name):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO Allergens (name) VALUES (?)", (name,))
    conn.commit()

def add_to_cart(conn, user_name, flavor_id, quantity):
    c = conn.cursor()
    c.execute("INSERT INTO Cart (user_name, flavor_id, quantity) SELECT?,?,? WHERE NOT EXISTS (SELECT 1 FROM Cart WHERE user_name=? AND flavor_id=?)", 
              (user_name, flavor_id, quantity, user_name, flavor_id))
    conn.commit()

def get_offering(conn, flavor_id):
    c = conn.cursor()
    c.execute("SELECT name, season, description FROM Flavors WHERE id=?", (flavor_id,))
    return c.fetchone()

def search_offering(conn, keyword):
    c = conn.cursor()
    c.execute("SELECT id, name, season, description FROM Flavors WHERE name LIKE?", ('%'+keyword+'%',))
    return c.fetchall()

def filter_by_allergy(conn, allergy):
    c = conn.cursor()
    c.execute("SELECT DISTINCT f.id, f.name, f.season, f.description FROM Flavors f LEFT JOIN Ingredients i ON f.id=i.flavor_id WHERE NOT EXISTS (SELECT 1 FROM Allergens a WHERE a.name=f.name) AND f.name NOT LIKE?", ('%'+allergy+'%',))
    return c.fetchall()

def main():
    conn = connect_to_db()
    while True:
        print("\n1. Add Flavor")
        print("2. Add Ingredient")
        print("3. Add Allergen")
        print("4. Add to Cart")
        print("5. Get Offering Details")
        print("6. Search Offerings")
        print("7. Filter by Allergy")
        print("8. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter flavor name: ")
            season = input("Enter season (optional): ")
            description = input("Enter description (optional): ")
            add_flavor(conn, name, season, description)
        elif choice == "2":
            name = input("Enter ingredient name: ")
            flavor_id = int(input("Enter flavor ID: "))
            add_ingredient(conn, name, flavor_id)
        elif choice == "3":
            name = input("Enter allergen name: ")
            add_allergen(conn, name)
        elif choice == "4":
            user_name = input("Enter your username: ")
            flavor_id = int(input("Enter flavor ID: "))
            quantity = int(input("Enter quantity: "))
            add_to_cart(conn, user_name, flavor_id, quantity)
        elif choice == "5":
            flavor_id = int(input("Enter flavor ID: "))
            offering = get_offering(conn, flavor_id)
            if offering:
                print(offering)
            else:
                print("Offering not found.")
        elif choice == "6":
            keyword = input("Enter search keyword: ")
            offerings = search_offering(conn, keyword)
            for offering in offerings:
                print(offering)
        elif choice == "7":
            allergy = input("Enter allergy concern: ")
            filtered_offerings = filter_by_allergy(conn, allergy)
            for offering in filtered_offerings:
                print(offering)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
