# Test Case: SMK-003 Search "Dior" returns Dior in first result

**ID:** SMK-003  
**Type:** Smoke  
**Priority:** High  
**Automation:** `tests/smoke/test_search.py::test_search_dior_shows_dior_in_first_title`

---

### Preconditions
- Website is available: https://makeupstore.com/

### Steps
1. Open https://makeupstore.com/
2. Click the search icon  
   Selector: `body > div.site-wrap > div.main-wrap > header > div.header-middle > div > div.header-left-row > div.search-button`
3. Type `dior` into input `#search-input` and start search (press Enter).
4. Wait for the first product card to appear  
   Card:  
   `body > div.site-wrap > div.main-wrap > div > div > div.catalog > div.catalog-content > div > div.catalog-products > ul > li:nth-child(1) > div.simple-slider-list__link > div.info-product-wrapper`  
   Title inside card:  
   `body > div.site-wrap > div.main-wrap > div > div > div.catalog > div.catalog-content > div > div.catalog-products > ul > li:nth-child(1) > div.simple-slider-list__link > div.info-product-wrapper > a`

### Expected Result
- The first product title contains the word **"dior"** (case-insensitive).

### Postconditions
- None.
