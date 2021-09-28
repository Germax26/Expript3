from typing import ClassVar
from exp_info import *

class CategoryList:
    def __init__(self, *categories):
        self.categories = categories
    
    def add(self, category):
        self.categories.append(category)

    def contains(self, category_name):
        for category in self.categories:
            if category.name == category_name:
                return True
        return False

    def get(self, category_name):
        for category in self.categories:
            if category.name == category_name:
                return category
        err = EnvironmentError(f"Category {category_name} does not exist.")
        raise err

class Category:
    """Category, used to store a 'category' of operators, all of which will have the same precedence in parsing. Multiple categories are used for more than one level of precedence."""
    def __init__(self, name, *tags):
        self.name = name
        self.tags = tags
        self.operators = {}

    def add(self, operator: str, python: type):
        """Add an operator to this category.

        Args:
            operator (str): The operator's signature.
            python (type): The operator's implementation class.

        Returns:
            Category: This category, with the new operator added in-place.
        """
        self.operators[operator] = python
        return self

    def display(self):
        """Display the category.
        """
        print("Name:", self.name)
        print("Tags:", self.tags)
        [print(operator) for operator in self.operators]

    def contains(self, operator: str) -> bool:
        """Checks if an operator is in this category by checking the signature.

        Args:
            operator (str): The signature of the operator.

        Returns:
            bool: Whether or not the operator is in this category
        """
        return operator in self.operators

    def __getitem__(self, index):
        return self.operators[index]

exp_category = module(__name__)

info = package_info(exp_category, "exp_category@v1 –– the built-in category package", [exp_info])

if __name__ == "__main__": info()