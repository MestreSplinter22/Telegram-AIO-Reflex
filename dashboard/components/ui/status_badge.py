import reflex as rx


def _badge(status: str):
    badge_mapping = {
        "Completed": ("check", "Sucesso", "bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 border-green-200 dark:border-green-800"),
        "Pending": ("loader", "Pendente", "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800"),
        "Canceled": ("ban", "Cancelado", "bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800"),
        "Failed": ("x", "Falha", "bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 border-red-200 dark:border-red-800"),
    }
    icon, text, class_name = badge_mapping.get(
        status, ("loader", "Pending", "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border-yellow-200 dark:border-yellow-800")
    )
    return rx.badge(
        rx.icon(icon, size=16, class_name="mr-1"),
        text,
        class_name=f"inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border {class_name}",
    )


def status_badge(status: str):
  return rx.match(
        status,
        ("completed", _badge("Completed")),
        ("pending", _badge("Pending")),
        ("canceled", _badge("Canceled")),
        ("failed", _badge("Failed")),
    )
