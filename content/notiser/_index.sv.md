+++
title = "Notiser"
description = "Korta notiser från leif.radio: morsenoveller, konditioner och annat smått."
outputs = ["HTML", "RSS"]

# Apply to item pages only so the section listing stays in the sitemap,
# while daily notiser stay out of the main RSS and home page lists.
[[cascade]]
  showHero = false
  showAuthor = false
  showReadingTime = false
  showWordCount = false
  showTableOfContents = false
  showTaxonomies = false
  showPagination = false
  [cascade.build]
    list = "local"
    render = "always"
  [cascade.target]
    kind = "page"
+++
