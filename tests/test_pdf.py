"""
Test Suite: PDF Report Generator.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tools.report_generator import generate_pdf

def test_pdf_generation():
    print("🧪 Test 1: PDF Generation")
    pdf_bytes = generate_pdf(
        report_text="## Summary\nTest property valued at ₹85L.\n## Recommendation\nBuy.\n## Disclaimer\nNot financial advice.",
        property_data={'City': 'Mumbai', 'State': 'Maharashtra', 'Property_Type': 'Apartment',
                       'BHK': 3, 'Size_in_SqFt': 1800, 'Furnished_Status': 'Semi-furnished',
                       'Security': 'Yes', 'Public_Transport_Accessibility': 'High'},
        comparables=[{'label': 'Smaller unit', 'bhk': 2, 'size_sqft': 1200, 'furnished': 'Semi',
                      'predicted_price_lakhs': 65.0, 'price_diff_pct': -23.5}],
        risk_data={'overall_risk_level': 'MODERATE', 'overall_risk_score': 40,
                   'risk_factors': [{'factor': 'Interest Rate', 'severity': 'MEDIUM', 'details': 'Test'}]}
    )
    assert isinstance(pdf_bytes, bytes), f"Expected bytes, got {type(pdf_bytes)}"
    assert len(pdf_bytes) > 1000, f"PDF too small ({len(pdf_bytes)} bytes)"
    assert pdf_bytes[:5] == b'%PDF-', "Not a valid PDF file"
    print(f"   ✅ Generated PDF: {len(pdf_bytes)} bytes")
    print(f"   ✅ Valid PDF header confirmed")

def test_pdf_without_optional_data():
    print("\n🧪 Test 2: PDF Without Optional Data")
    pdf_bytes = generate_pdf(report_text="Simple report text only.")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    print(f"   ✅ Minimal PDF: {len(pdf_bytes)} bytes")

if __name__ == "__main__":
    print("=" * 50)
    print("  PDF REPORT GENERATOR TEST SUITE")
    print("=" * 50)
    test_pdf_generation()
    test_pdf_without_optional_data()
    print("\n  🎉 ALL PDF TESTS PASSED!")
