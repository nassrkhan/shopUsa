import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException

def start_checkout():
    url = url_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    credit_card_number = credit_card_number_entry.get()
    expiration_month = expiration_month_entry.get()
    expiration_year = expiration_year_entry.get()
    cvv = cvv_entry.get()

    while True:
            try:
                # driver = webdriver.Firefox()
                driver = webdriver.Chrome()
                driver.get(url)
                wait = WebDriverWait(driver, 20)

                select_element = wait.until(EC.element_to_be_clickable((By.ID, "quantity")))
                select = Select(select_element)
                options = select.options
                max_value = sorted([int(option.text) for option in options])[-1]

                for _ in range(3):
                    try:
                        select.select_by_visible_text(str(max_value))
                        break
                    except ElementClickInterceptedException:
                        print("ElementClickInterceptedException occurred. Retrying...")
                        continue
                else:
                    raise ElementClickInterceptedException("Failed to select option after multiple retries")

                element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.col-md-12:nth-child(5) > button:nth-child(1)")))
                element.click()

                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#checkout"))).click()

                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".checkout-top-text > p:nth-child(1) > a:nth-child(1)"))).click()

                email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.form-group:nth-child(3) > label:nth-child(1) > input:nth-child(2)")))
                email_input.send_keys(email)

                password_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#registria_form_login > div:nth-child(4) > label:nth-child(1) > input:nth-child(2)")))
                password_input.send_keys(password)

                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#registria_form_login > div:nth-child(5) > button:nth-child(1)"))).click()

                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#shipping_save"))).click()
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#shipping_method_save"))).click()
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#billing_save"))).click()

                card_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#credit_card_number")))
                card_input.send_keys(credit_card_number)

                cc_month_select = Select(wait.until(EC.visibility_of_element_located((By.ID, "credit_card_month"))))
                cc_month_select.select_by_value(expiration_month)
                cc_year_select = Select(wait.until(EC.visibility_of_element_located((By.ID, "credit_card_year"))))
                cc_year_select.select_by_value(expiration_year)

                cvv_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#credit_card_cvv")))
                cvv_input.send_keys(cvv)
                wait = WebDriverWait(driver, 10)
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#payment_method_save"))).click()

                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn:nth-child(4)"))).click()
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                driver.quit()  
                continue 

root = tk.Tk()
root.title("Automated Checkout")

window_width = 400
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

ttk.Label(frame, text="URL:").grid(row=0, column=0, sticky="w")
url_entry = ttk.Entry(frame, width=40)
url_entry.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="w")
email_entry = ttk.Entry(frame, width=40)
email_entry.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky="w")
password_entry = ttk.Entry(frame, width=40, show="*")
password_entry.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Credit Card Number:").grid(row=3, column=0, sticky="w")
credit_card_number_entry = ttk.Entry(frame, width=40)
credit_card_number_entry.grid(row=3, column=1, pady=5)

ttk.Label(frame, text="Expiration Month:").grid(row=4, column=0, sticky="w")
expiration_month_entry = ttk.Entry(frame, width=40)
expiration_month_entry.grid(row=4, column=1, pady=5)

ttk.Label(frame, text="Expiration Year:").grid(row=5, column=0, sticky="w")
expiration_year_entry = ttk.Entry(frame, width=40)
expiration_year_entry.grid(row=5, column=1, pady=5)

ttk.Label(frame, text="CVV:").grid(row=6, column=0, sticky="w")
cvv_entry = ttk.Entry(frame, width=40)
cvv_entry.grid(row=6, column=1, pady=5)

checkout_button = ttk.Button(frame, text="Start Checkout", command=start_checkout)
checkout_button.grid(row=7, columnspan=2, pady=10)

root.mainloop()
