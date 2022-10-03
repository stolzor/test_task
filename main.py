from model import ParserFields


def main():
    driver = ParserFields()
    print(driver.parse_necessary_fields('https://www.aceee.org/blog-post/2021/08/five-states-set-appliance-efficiency-standards-banner-year'))
    driver.quit()


if __name__ == "__main__":
    main()
