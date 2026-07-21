"""
Phase 10.9 Full System Integration Test

Tests the complete Windows automation subsystem.

Safe:
- Uses dry_run for power operations.
- Restores system state where practical.
"""

from __future__ import annotations

from pathlib import Path

from app.system.system_manager import SystemManager


LINE = "=" * 70


def section(title: str) -> None:
    print("\n" + LINE)
    print(title)
    print(LINE)


def main() -> None:

    sm = SystemManager()

    print(LINE)
    print("PHASE 10.9 SYSTEM INTEGRATION TEST")
    print(LINE)

    passed = 0
    failed = 0

    # --------------------------------------------------
    section("Health Check")

    try:
        print(sm.health_check())
        passed += 1
    except Exception as e:
        print(e)
        failed += 1

    # --------------------------------------------------
    section("Application Manager")

    try:

        print(sm.open_application("notepad"))

        running = sm.application_running("notepad")

        print("Running:", running)

        input("\nPress ENTER to close Notepad...")

        print(sm.close_application("notepad"))

        passed += 1

    except Exception as e:

        print(e)

        failed += 1

    # --------------------------------------------------
    section("File Manager")

    try:

        root = Path.home() / "Desktop" / "Jarvis_Test"

        hello = root / "hello.txt"

        world = root / "world.txt"

        copy = root / "copy.txt"

        moved = root / "moved.txt"

        print(sm.create_folder(str(root)))

        print(sm.create_file(str(hello)))

        print(sm.rename_path(str(hello), str(world)))

        print(sm.copy_path(str(world), str(copy)))

        print(sm.move_path(str(copy), str(moved)))

        print(sm.list_directory(str(root)))

        input("\nPress ENTER to delete test folder...")

        print(sm.delete_path(str(root)))

        passed += 1

    except Exception as e:

        print(e)

        failed += 1

    # --------------------------------------------------
    section("Volume Manager")

    try:

        original = sm.get_volume()

        print("Original:", original)

        print(sm.set_volume(30))

        input("\nENTER")

        print(sm.increase_volume(20))

        input("\nENTER")

        print(sm.decrease_volume(10))

        input("\nENTER")

        print(sm.mute())

        print("Muted:", sm.is_muted())

        input("\nENTER")

        print(sm.unmute())

        sm.set_volume(original)

        print("Restored:", original)

        passed += 1

    except Exception as e:

        print(e)

        failed += 1

    # --------------------------------------------------
    section("Brightness Manager")

    try:

        original = sm.get_brightness()

        print("Original:", original)

        print(sm.set_brightness(40))

        input("\nENTER")

        print(sm.increase_brightness(20))

        input("\nENTER")

        print(sm.decrease_brightness(10))

        sm.set_brightness(original)

        print("Restored:", original)

        passed += 1

    except Exception as e:

        print(e)

        failed += 1

    # --------------------------------------------------
    section("Clipboard Manager")

    try:

        original = sm.paste_text()

        print(sm.copy_text("Hello JARVIS"))

        print(sm.paste_text())

        print(sm.clear_clipboard())

        print(repr(sm.paste_text()))

        sm.copy_text(original)

        passed += 1

    except Exception as e:

        print(e)

        failed += 1

    # --------------------------------------------------
    section("Screenshot Manager")

    try:

        print(sm.take_screenshot())

        print(sm.open_last_screenshot())

        passed += 1

    except Exception as e:

        print(e)

        failed += 1

    # --------------------------------------------------
    section("Power Manager")

    try:

        print(sm.shutdown(
            delay=60,
            dry_run=True,
        ))

        print(sm.restart(
            delay=60,
            dry_run=True,
        ))

        print(sm.lock(
            dry_run=True,
        ))

        print(sm.sleep(
            dry_run=True,
        ))

        print(sm.hibernate(
            dry_run=True,
        ))

        print(sm.logoff(
            dry_run=True,
        ))

        print(sm.cancel_shutdown())

        passed += 1

    except Exception as e:

        print(e)

        failed += 1

    # --------------------------------------------------

    print("\n" + LINE)
    print("FINAL REPORT")
    print(LINE)

    print(f"Passed : {passed}")
    print(f"Failed : {failed}")

    if failed == 0:

        print("\n🎉 PHASE 10.9 PASSED")

    else:

        print("\n❌ PHASE 10.9 FAILED")

    print(LINE)


if __name__ == "__main__":
    main()