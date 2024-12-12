from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from collections import deque
import os
import pandas as pd
import time
import requests

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ 
        Leave this method as is! It will be over-written the child classes
        Each child class should perform the following:
            Record the node value in self.order AND return its children
            parameter: node
            return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

        
    def dfs_search(self, node):
        # 1. clear out visited set and order list
        self.visited.clear()
        self.order.clear()      
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)
        
    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        
        # 3. call self.visit_and_get_children(node) to get the children
        children= self.visit_and_get_children(node)
        
        # 4. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
 # --------------------------------------------------------------------------------------------------------------       

    def bfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        self.bfs_visit(node)
        
    def bfs_visit(self, node):
        queue = [node]
        while queue:
            current_node = queue.pop(0)
            if current_node in self.visited:
                continue
            self.visited.add(current_node)
            children = self.visit_and_get_children(current_node)
            for child in children:
                if child not in self.visited:
                    queue.append(child)
#     def bfs_search(self, graph, node):
#         # 1. clear out visited set and order list
#         self.visited.clear()
#         self.order.clear()
        # queue = deque()                
#         self.visited[node] = True
#         queue.append(node)
#         while queue:
#             s = queue.popleft()       
#             for i in self.order[node]:
#                 if not self.visited[i]:
#                     queue.append(i)
#                     self.visited[i] = True
        
        # https://www.geeksforgeeks.org/difference-between-bfs-and-dfs/
        
        # --------------------------------------------------------------------------------------------------------------
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        self.order.append(node)
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        for child, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(child)
        return children
# --------------------------------------------------------------------------------------------------------------
class FileSearcher(GraphSearcher):
    def __init__(self):
         super().__init__()

    def visit_and_get_children(self, node):
        file_path = os.path.join("file_nodes", node)
        with open(file_path, "r") as file:
            node_val = file.readline().strip()
            self.order.append(node_val)
            child_line = file.readline().strip()
            if child_line:
                children = [child.strip() for child in child_line.split(",")]
            else:
                children = []
        return children
              
#         self.order.append(node)
#         if os.path.isdir(node):
#             try:
#                 return [os.path.join(node, child) for child in os.listdir(node)]
    #         else:
    #             return []
  
    def concat_order(self):
        return "".join(str(item) for item in self.order)
    # --------------------------------------------------------------------------------------------------------------
class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.fragments = []
        
    def visit_and_get_children(self, url):
        self.driver.get(url)
        
        links = self.driver.find_elements(By.TAG_NAME, 'a')
        children = [link.get_attribute('href') for link in links if link.get_attribute('href')]
        
        tables = pd.read_html(url)
        # if not tables.empty:
        #     self.fragments.extend(tables)
        self.fragments.extend(tables)
        self.order.append(url)
        return children
    
    def table(self):
        if not self.fragments:
            return pd.DataFrame()
        self.fragments = [table for table in self.fragments if not table.empty]
        return pd.concat(self.fragments, ignore_index = True)
    
    
      # --------------------------------------------------------------------------------------------------------------
def reveal_secrets(driver, url, travellog):
    password = ''.join(str(num) for num in travellog['clue'].tolist())
                           
    driver.get(url)
                           
            
    first_textbox = driver.find_element(By.ID, 'password-textbox')
    first_go_button = driver.find_element(By.ID, 'submit-button')
    first_textbox.send_keys(password)
    first_go_button.click()
        
    time.sleep(3)
    
    view_location_button = driver.find_element(By.ID, 'location-button')
    view_location_button.click()
        
    time.sleep(5)
        
    img_extract = driver.find_element(By.ID, 'image').get_attribute("src")
    img_save = requests.get(img_extract)
    if img_save.status_code == 200:
        with open("Current_Location.jpg", "wb") as f:
            f.write(img_save.content)
    # img_save = requests.get("https://badgerherald.com/wp-content/uploads/2016/02/aerial_stadium_fball13_6828.jpg") 
    location_txt = driver.find_element(By.ID, 'location').text
        
    return location_txt
        
        
        
        