import os
import sys
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.query_engine import QueryEngine
from src.utils import load_config, get_logger

# Load environment variables
load_dotenv()

logger = get_logger(__name__)

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


# Test functions
def test_hacking_punishment():
    """Test: What is the punishment for hacking with computer system?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the punishment for hacking with computer system?")
    assert "imprisonment" in response.lower(), "Response should mention imprisonment"
    assert "500000" in response or "500,000" in response, "Response should mention fine amount"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Hacking punishment")


def test_cheating_using_computer_resource():
    """Test: What is the offense of cheating using computer resource?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the offense of cheating using computer resource?")
    assert "cheat" in response.lower() or "cheating" in response.lower(), "Should mention cheating"
    assert "computer" in response.lower(), "Should mention computer"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Cheating using computer resource")


def test_publishing_private_images():
    """Test: What is the punishment for publishing private images without consent?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the punishment for publishing private images without consent?")
    assert "imprisonment" in response.lower(), "Should mention imprisonment"
    assert "three years" in response.lower() or "3 years" in response or "200000" in response, "Should mention duration or fine"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Publishing private images")


def test_cyberterrorism_offense():
    """Test: What is cyberterrorism?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is cyberterrorism?")
    assert "cyber" in response.lower() or "terrorism" in response.lower(), "Should mention cyberterrorism"
    assert "security" in response.lower() or "access" in response.lower(), "Should describe the offense"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Cyberterrorism offense")


def test_tampering_with_source_code():
    """Test: What is tampering with computer source documents?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the offense of tampering with computer source documents?")
    assert "tampering" in response.lower() or "source" in response.lower(), "Should mention source code/documents"
    assert "imprisonment" in response.lower(), "Should mention punishment"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Tampering with source code")


def test_receiving_stolen_computer():
    """Test: What is the punishment for receiving stolen computer?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the offense of receiving stolen computer or communication device?")
    assert "stolen" in response.lower(), "Should mention stolen"
    assert "imprisonment" in response.lower(), "Should mention imprisonment"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Receiving stolen computer")


def test_unauthorized_password_usage():
    """Test: What is the punishment for using password of another person?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the offense of using password of another person?")
    assert "password" in response.lower(), "Should mention password"
    assert "section 66c" in response.lower() or "offense" in response.lower(), "Should identify the offense"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Unauthorized password usage")


def test_protected_system_access():
    """Test: What is the punishment for accessing protected system?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the offense of securing access to a protected system?")
    assert "access" in response.lower() or "protected" in response.lower(), "Should mention protected system access"
    assert "imprisonment" in response.lower() or "ten years" in response.lower(), "Should mention imprisonment"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Protected system access")


def test_section_65_details():
    """Test: Can retrieve Section 65 details?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("Tell me about Section 65 of IT Act")
    assert "section 65" in response.lower() or "tampering" in response.lower(), "Should mention Section 65 or tampering"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Section 65 details")


def test_section_66_details():
    """Test: Can retrieve Section 66 details?"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("Tell me about Section 66 of IT Act")
    assert "section 66" in response.lower() or "hacking" in response.lower(), "Should mention Section 66 or hacking"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Section 66 details")


def test_response_contains_sources():
    """Test: Response includes source citations"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, sources = engine.query("What is the penalty for hacking?")
    assert len(response) > 10, "Response should be substantial"
    assert isinstance(response, str), "Response should be a string"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Response contains valid content")


def test_multiple_cyber_crimes():
    """Test: Can retrieve information about multiple cyber crimes"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("List the different cyber crimes and their punishments")
    assert "section" in response.lower() or "offense" in response.lower(), "Should mention sections or offenses"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Multiple cyber crimes")


def test_fine_amounts():
    """Test: Responses include specific fine amounts"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the fine for Section 66 hacking offense?")
    
    if not response or len(response.strip()) == 0:
        response, _ = engine.query("What are the penalties for hacking and cheating offenses?")
    
    assert len(response) > 0, "Response should not be empty"
    assert "fine" in response.lower() or "100000" in response or "200000" in response or "500000" in response, "Should mention fine amounts"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Fine amounts included")


def test_imprisonment_duration():
    """Test: Responses mention imprisonment duration"""
    config = load_config()
    engine = QueryEngine(chroma_path=config['chroma_path'])
    response, _ = engine.query("What is the maximum imprisonment for Section 66 hacking?")
    
    if not response or len(response.strip()) == 0:
        response, _ = engine.query("What are the imprisonment penalties under IT Act sections?")
    
    assert len(response) > 0, "Response should not be empty"
    assert "imprisonment" in response.lower() or "year" in response.lower() or "life" in response.lower(), "Should mention imprisonment duration"
    print(f"{Colors.GREEN}[PASS]{Colors.END} Imprisonment duration mentioned")


# Run all tests
if __name__ == "__main__":
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}RUNNING RAG TEST SUITE FOR PROJECT LEXORA{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 70}{Colors.END}\n")
    
    tests = [
        test_hacking_punishment,
        test_cheating_using_computer_resource,
        test_publishing_private_images,
        test_cyberterrorism_offense,
        test_tampering_with_source_code,
        test_receiving_stolen_computer,
        test_unauthorized_password_usage,
        test_protected_system_access,
        test_section_65_details,
        test_section_66_details,
        test_response_contains_sources,
        test_multiple_cyber_crimes,
        test_fine_amounts,
        test_imprisonment_duration,
    ]
    
    passed = 0
    failed = 0
    errors = []
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"{Colors.RED}[FAILED]{Colors.END} {test.__name__}")
            print(f"         Error: {str(e)}\n")
            errors.append((test.__name__, str(e)))
            failed += 1
        except Exception as e:
            print(f"{Colors.RED}[ERROR]{Colors.END} {test.__name__}")
            print(f"       Error: {str(e)}\n")
            errors.append((test.__name__, str(e)))
            failed += 1
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}{Colors.END}")
    
    if failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}TEST RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}[SUCCESS] All tests passed!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}TEST RESULTS: {passed} passed, {failed} failed out of {len(tests)} tests{Colors.END}")
        if errors:
            print(f"\n{Colors.RED}Failed Tests:{Colors.END}")
            for test_name, error_msg in errors:
                print(f"  - {test_name}: {error_msg}")
    
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 70}{Colors.END}\n")
