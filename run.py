from app import app

# checks if the script is being executed directly 
# (not being imported as a module into another script)
if __name__ == '__main__':
    # starts the Flask development server with the debug mode enabled. 
    # The debug=True argument enables several helpful features during development
    app.run(debug=True)
