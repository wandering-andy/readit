# Copyright (C) 2017, 2018 projectreadit organization and contributors.
# This file is part of Readit - Command Line Bookmark Manager Tool.
#
# This project is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with readit.  If not, see <http://www.gnu.org/licenses/>.
import sys  # used to exit from system

import click  # used for command line interface.
import requests  # to check whether url is valid or not

from readit import database  # used to perform database operations.
from readit.commands import view  # Used to show results to users

database_connection = database.DatabaseConnection()
output = view.ShowResults()


@click.command()
@click.command("--add", "-a", nargs=0, help="Add URLs with space-separated")
def add(urls_to_add):
    for url_to_add in urls_to_add:
        url = url_to_add
        try:
            validate_url = requests.get(url)
            validate_code = validate_url.status_code
            if validate_code == 200:
                is_url_added = database_connection.add_url(url)
                if is_url_added:
                    print("Bookmarked.")
                else:
                    print("URL is already bookmarked. Check URL information. See help")
            else:
                print("*" * 12, "\nInvalid URL\n", "*" * 11)
                if option_yes_no():
                    is_url_added = database_connection.add_url(url)
                    if is_url_added:
                        print("Bookmarked.")
                    else:
                        print(
                            "URL is already bookmarked. Check URL information. See help"
                        )
        except Exception:
            print("*" * 12, "\nInvalid URL\n", "*" * 11)
            if option_yes_no():
                is_url_added = database_connection.add_url(url)
                if is_url_added:
                    print("Bookmarked.")
                else:
                    print("URL is already bookmarked. Check URL information. See help")


@click.command("--tag", "-t", nargs=2, help="Add Tag with space-separated URL")
def tag():
    tag_list = []
    for tag_to_url in tag:
        tag_list.append(tag_to_url)
    tag_name = tag_list[0]
    tagged_url = tag_list[1]
    try:
        validate_url = requests.get(tagged_url)
        validate_code = validate_url.status_code
        if validate_code == 200:
            is_url_tagged = database_connection.tag_url(tag_name, tagged_url)
            if is_url_tagged:
                print("Bookmarked URL with tag.")
            else:
                print(
                    "URL is already bookmarked with tag. Check URL information. See help"
                )
        else:
            print("*" * 12, "\nInvalid URL\n", "*" * 11)
            if option_yes_no():
                is_url_tagged = database_connection.tag_url(tag_name, tagged_url)
                if is_url_tagged:
                    print("Bookmarked URL with tag.")
                else:
                    print(
                        "URL is already bookmarked with tag. Check URL information. See help"
                    )
    except Exception:
        print("*" * 12, "\nInvalid URL\n", "*" * 11)
        if option_yes_no():
            is_url_tagged = database_connection.tag_url(tag_name, tagged_url)
            if is_url_tagged:
                print("Bookmarked URL with tag.")
            else:
                print(
                    "URL is already bookmarked with tag. Check URL information. See help"
                )


@click.command("--delete", "-d", nargs=1, help="Remove a URL of particular ID")
def delete():
    is_url_deleted = database_connection.delete_url(delete)
    if is_url_deleted:
        print("URL deleted.")
    else:
        print("URL of this id is not present in database.")


@click.command("--clear", "-c", multiple=True, nargs=0, help="Clear bookmarks")
def clear():
    is_db_clear = database_connection.delete_all_url()
    if is_db_clear:
        print("All bookmarks deleted.")
    else:
        print("Database does not have any data.")


@click.command("--update", "-u", nargs=2, help="Update a URL for specific ID")
def update():
    url_list = []
    for update_to_url in update:
        url_list.append(update_to_url)
    url_id = url_list[0]
    url = url_list[1]
    try:
        validate_url = requests.get(url)
        validate_code = validate_url.status_code
        if validate_code == 200:
            is_url_updated = database_connection.update_url(url_id, url)
            if is_url_updated:
                print("URL of this id updated.")
            else:
                print("Provided id is not present or same URL is already in available.")
        else:
            print("*" * 12, "\nInvalid URL\n", "*" * 11)
            if option_yes_no():
                is_url_updated = database_connection.update_url(url_id, url)
                if is_url_updated:
                    print("URL of this id updated.")
                else:
                    print(
                        "Provided id is not present or same URL is already in available."
                    )
    except Exception:
        print("*" * 12, "\nInvalid URL\n", "*" * 11)
        if option_yes_no():
            is_url_updated = database_connection.update_url(url_id, url)
            if is_url_updated:
                print("URL of this id updated.")
            else:
                print("Provided id is not present or same URL is already in available.")


@click.command("--search", "-s", nargs=1, help="Search all bookmarks by Tag")
def search():
    output.print_bookmarks(database_connection.search_url(search))


@click.command("--view", "-v", multiple=True, nargs=0, help="Show bookmarks")
def view():
    output.print_bookmarks(database_connection.show_url())


@click.command("--openurl", "-o", nargs=1, help="Open URL in Browser")
def openurl():
    database_connection.open_url(openurl)


@click.command("--version", "-V", is_flag=True, help="Check latest version")
def version():
    print("readit v0.4.0")


@click.command("--export", "-e", multiple=True, nargs=0, help="Export URLs in csv file")
def export():
    path = database_connection.export_urls()
    msg = "Exported bookmarks available at"
    if path:
        path = "{} {}".format(msg, path)
        print(path)
    else:
        print("Bookmarks are not exported in csv file.")


@click.command("--taglist", "-tl", multiple=True, nargs=0, help="Show all Tags")
def taglist():
    output.print_all_tags(database_connection.list_all_tags())


@click.command("--urlinfo", "-ui", nargs=1, help="Check particular URL information")
def urlinfo():
    output.print_bookmarks(database_connection.url_info(urlinfo))


@click.command("insert", nargs=-1, required=False)
def insert():
    for url_to_add in insert:
        url = url_to_add
        try:
            validate_url = requests.get(url)
            validate_code = validate_url.status_code
            if validate_code == 200:
                is_url_added = database_connection.add_url(url)
                if is_url_added:
                    print("Bookmarked.")
                else:
                    print("URL is already bookmarked. Check URL information. See help")
            else:
                print("*" * 12, "\nInvalid URL\n", "*" * 11)
                if option_yes_no():
                    is_url_added = database_connection.add_url(url)
                    if is_url_added:
                        print("Bookmarked.")
                    else:
                        print(
                            "URL is already bookmarked. Check URL information. See help"
                        )

        except Exception:
            print("*" * 12, "\nInvalid URL\n", "*" * 11)
            if option_yes_no():
                is_url_added = database_connection.add_url(url)
                if is_url_added:
                    print("Bookmarked.")
                else:
                    print("URL is already bookmarked. Check URL information. See help")


def option_yes_no():
    """
    Asks whether to bookmark invalid URLs or Offline URLs to database.
    """
    option = input("Still you want to bookmark: Yes/No ? ")
    if option.lower() in ["yes", "y"]:
        return True
    else:
        sys.exit(0)


def main():
    """
    Readit - Command-line bookmark manager tool.
    """
    insert()
    add()
    tag()
    delete()
    clear()
    update()
    search()
    view()
    openurl()
    version()
    export()
    taglist()
    urlinfo()
