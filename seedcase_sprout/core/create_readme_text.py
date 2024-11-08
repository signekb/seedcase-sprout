def create_readme_text(properties: dict) -> str:
    """Create a json object containing the readme text.

    Args:
      properties: An object containing the package and resource properties.

    Returns:
      A string for the README text
    """
    # TODO: Finish this once Properties have been finished.
    # resources = # Python code to convert the resource details in the dict as
    # a Markdown list.

    readme_text = (
        f"# {properties["name"]}: {properties["title"]}\n\n"
        f"{properties["description"]}\n\n"
        f"There are {len(properties["resources"])} resources in this package."
    )
    return readme_text
