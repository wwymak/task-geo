from task_geo.data_sources.demographics.it_census import it_census_connector, it_census_formatter


def main():
    data = it_census_connector()
    df = it_census_formatter(data)
    df.head()


if __name__ == '__main__':
    main()
