import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementClickInterceptedException

def main():

    st.title("Automated Checkout Bot")
    st.write("Fill out the form below to proceed with the automated checkout.")

    # url = st.text_input("Enter URL", "https://shopusa.fujifilm-x.com/products/0-74101-20596-1")
    url = st.text_input("Enter URL", "")
    email = st.text_input("Enter Email", "")
    password = st.text_input("Enter Password", "", type="password")
    credit_card_number = st.text_input("Credit Card Number", "")
    expiration_month = st.selectbox("Expiration Month", [str(i).zfill(2) for i in range(1, 13)])
    expiration_year = st.selectbox("Expiration Year", [str(i) for i in range(2022, 2030)])
    cvv = st.text_input("CVV", "")

    if st.button("Start Checkout"):
        while True:
            try:
                # driver = webdriver.Firefox()
                driver = webdriver.Chrome()
                driver.get(url)
                wait = WebDriverWait(driver, 20)

                # select_element = wait.until(EC.element_to_be_clickable((By.ID, "quantity")))
                # select = Select(select_element)
                # # select.select_by_visible_text("2")

                # for _ in range(3):
                #     try:
                #         select.select_by_visible_text("2")
                #         break
                #     except ElementClickInterceptedException:
                #         print("ElementClickInterceptedException occurred. Retrying...")
                #         continue
                # else:
                #     raise ElementClickInterceptedException("Failed to select option after multiple retries")

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

                st.success("Checkout completed successfully!")
                break
            except Exception as e:
                st.error(f"An error occurred: {e}")
                if 'driver' in locals():
                    driver.quit()
                continue

if __name__ == "__main__":
    main()
