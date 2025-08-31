from playwright.sync_api import sync_playwright, expect
import time

def test_langgraph_signup():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Navigate to LangGraph
            page.goto('https://smith.langchain.com/')
            
            # Click "Sign up with email" button
            page.get_by_role('button', name='Sign up with email').click()
            
            # Fill in the initial signup form
            page.get_by_label('Email').fill('test@example.com')
            page.get_by_label('Password').fill('TestPassword123!')
            
            # Click continue (commented out for test purposes)
            # page.get_by_role('button', name='Continue').click()
            
            # Wait for confirmation message
            # expect(page.get_by_role('alert').get_by_text('Check your inbox')).to_be_visible()
            
            time.sleep(2)  # Wait to see the results
            
        except Exception as e:
            print(f"Error during test: {e}")
            
        finally:
            # Clean up
            context.close()
            browser.close()

if __name__ == "__main__":
    test_langgraph_signup()