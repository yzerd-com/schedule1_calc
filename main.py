from precompute import load_precomputed
from web_template import generate_static_html
from config import AVAILABLE_LEVELS, BASE_PRODUCT_NAMES

def main():
    precomputed = load_precomputed()
    generate_static_html(precomputed, AVAILABLE_LEVELS, BASE_PRODUCT_NAMES)

if __name__ == "__main__":
    main()
