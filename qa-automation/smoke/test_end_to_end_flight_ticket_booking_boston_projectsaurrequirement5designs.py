# Target file: tests/test_end_to_end_flight_ticket_booking_boston_to_london.py
# Generated execution model:
# - language: python
# - test_framework: pytest
# - playwright_api: sync_api
# Run completion: FULL
# Future page files:
# - pages/home_page.py
# - pages/content_page.py

import pytest
import re
from playwright.sync_api import Page, expect

@pytest.fixture
def vtest_base_url() -> str:
    return 'https://blazedemo.com'

@pytest.fixture
def test_data() -> dict:
    return {
        'name': 'Ada Lovelace',
        'address': '10 Downing Street',
        'destination_city': 'London',
        'state': 'Greater London',
        'zip': 'SW1A 2AA',
        'card_number': '4111111111111111',
    }

class HomePage:
    PAGE_TYPE = 'home'
    LOCATOR_1 = 'select[name="fromPort"]'
    LOCATOR_2 = 'select[name="toPort"]'
    LOCATOR_3 = 'input.btn'

    def enter_boston_into_the_departure_city_field(self, page: Page, test_data: dict) -> None:
        page.locator('select[name="fromPort"]').select_option('Boston')

    def enter_london_into_the_destination_city_field(self, page: Page, test_data: dict) -> None:
        page.locator('select[name="toPort"]').select_option('London')

    def click_the_find_flights_button(self, page: Page, test_data: dict) -> None:
        page.locator('input.btn').click()


class ContentPage:
    PAGE_TYPE = 'content'
    LOCATOR_1 = 'body:nth-of-type(1) > div:nth-of-type(2) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1) > input:nth-of-type(1)'
    LOCATOR_2 = '#inputName'
    LOCATOR_3 = '#address'
    LOCATOR_4 = '#city'
    LOCATOR_5 = '#state'
    LOCATOR_6 = '#zipCode'
    LOCATOR_7 = '#cardType'
    LOCATOR_8 = '#creditCardNumber'
    LOCATOR_9 = '#nameOnCard'
    LOCATOR_10 = 'input.btn'

    def click_the_select_flight_button_for_the_first_listed_flight(self, page: Page, test_data: dict) -> None:
        page.locator('body:nth-of-type(1) > div:nth-of-type(2) > table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(1) > td:nth-of-type(1) > input:nth-of-type(1)').click()

    def enter_ada_lovelace_into_the_name_field(self, page: Page, test_data: dict) -> None:
        page.locator('#inputName').fill(test_data['name'])
        expect(page.locator('#inputName')).to_have_value(test_data['name'])

    def enter_10_downing_street_into_the_address_field(self, page: Page, test_data: dict) -> None:
        page.locator('#address').fill(test_data['address'])
        expect(page.locator('#address')).to_have_value(test_data['address'])

    def enter_london_into_the_city_field(self, page: Page, test_data: dict) -> None:
        page.locator('#city').fill(test_data['destination_city'])
        expect(page.locator('#city')).to_have_value(test_data['destination_city'])

    def enter_greater_london_into_the_state_field(self, page: Page, test_data: dict) -> None:
        page.locator('#state').fill(test_data['state'])
        expect(page.locator('#state')).to_have_value(test_data['state'])

    def enter_sw1a_2aa_into_the_zip_code_field(self, page: Page, test_data: dict) -> None:
        page.locator('#zipCode').fill(test_data['zip'])
        expect(page.locator('#zipCode')).to_have_value(test_data['zip'])

    def select_visa_as_the_card_type(self, page: Page, test_data: dict) -> None:
        page.locator('#cardType').select_option('Visa')

    def enter_4111111111111111_into_the_card_number_field(self, page: Page, test_data: dict) -> None:
        page.locator('#creditCardNumber').fill(test_data['card_number'])
        expect(page.locator('#creditCardNumber')).to_have_value(test_data['card_number'])

    def enter_ada_lovelace_into_the_name_on_card_field(self, page: Page, test_data: dict) -> None:
        page.locator('#nameOnCard').fill(test_data['name'])
        expect(page.locator('#nameOnCard')).to_have_value(test_data['name'])

    def click_the_purchase_flight_button(self, page: Page, test_data: dict) -> None:
        page.locator('input.btn').click()


def test_end_to_end_flight_ticket_booking_boston_to_london(page: Page, vtest_base_url: str, test_data: dict) -> None:
    page.goto(vtest_base_url)

    home_page = HomePage()
    content_page = ContentPage()

    home_page.enter_boston_into_the_departure_city_field(page, test_data)
    home_page.enter_london_into_the_destination_city_field(page, test_data)
    home_page.click_the_find_flights_button(page, test_data)
    content_page.click_the_select_flight_button_for_the_first_listed_flight(page, test_data)
    content_page.enter_ada_lovelace_into_the_name_field(page, test_data)
    content_page.enter_10_downing_street_into_the_address_field(page, test_data)
    content_page.enter_london_into_the_city_field(page, test_data)
    content_page.enter_greater_london_into_the_state_field(page, test_data)
    content_page.enter_sw1a_2aa_into_the_zip_code_field(page, test_data)
    content_page.select_visa_as_the_card_type(page, test_data)
    content_page.enter_4111111111111111_into_the_card_number_field(page, test_data)
    content_page.enter_ada_lovelace_into_the_name_on_card_field(page, test_data)
    content_page.click_the_purchase_flight_button(page, test_data)

    assert 'confirmation.php' in page.url
    expect(page.locator('body')).to_contain_text('Thank you for your purchase today!')
