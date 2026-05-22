def Ui() -> None:
    print("=== a-maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Quit")
    try:
        param = input("Choice? (1-4): ")
        if param == "1":
            print("Re-generate a new maze")
        elif param == "2":
            print("Show/Hide path from entry to exit")
        elif param == "3":
            print("Rotate maze colors")
        elif param == "4":
            print("Quiting...")
            return
        else:
            print("Invalid input, Quiting...")
            return
    except KeyboardInterrupt:
        print("\nError input, Quiting...")
        exit()
