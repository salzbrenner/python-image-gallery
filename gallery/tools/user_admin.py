import db


def prompt_user():
    res = input("""
1) List users
2) Add user
3) Edit user
4) Delete user
5) Quit
Enter command> """)
    try:
        n = int(res)
        if 1 <= n <= 5:
            return handle_choice(n)
        return prompt_user()
    except:
        return prompt_user()


def handle_choice(n):
    if n == 1:
        list_users()
    elif n == 2:
        add_user()
    elif n == 3:
        edit_user()
    elif n == 4:
        delete_user()
    elif n == 5:
        return False
    return True


def list_users():
    q = db.get_users()
    _f = '{0:<20} {1:<20} {2:<20}'
    print(_f.format('username', 'password', 'full name'))
    print('----------------------------------------------------')
    for row in q:
        print(_f.format(*row))


def add_user():
    username = input('Username> ')
    pw = input('Password> ')
    full_name = input('Full name> ')

    if not db.add_user(username, pw, full_name):
        print()
        print(f'Error: user with username {username} already exists')


def edit_user():
    username = input('Username to edit> ')

    if not db.get_single_user(username):
        print()
        print('No such user.')
        return

    pw = input('New password (press enter to keep current)> ')
    full_name = input('New full name (press enter to keep current)> ')
    db.edit_user(username, pw, full_name)


def delete_user():
    username = input('Enter username to delete> ')

    if not db.get_single_user(username):
        return

    confirm_string = f'Are you sure you want to delete {username} (yes/no)? '
    print()
    confirm = input(confirm_string).lower()

    while confirm != 'yes'.lower() and confirm != 'no'.lower():
        print()
        print('Please type yes or no')
        confirm = input(confirm_string).lower()

    if confirm == 'no':
        return

    if db.delete_user(username):
        print()
        print('Deleted.')


def main():
    db.connect()
    valid = True
    while valid:
        valid = prompt_user()
    print()
    print('Bye.')


if __name__ == '__main__':
    main()
