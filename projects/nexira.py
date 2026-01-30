import time
from projects.base_project import BaseProject

CHECKIN_XPATH = '//*[@id="__next"]/div/div[3]/div[1]/ul/li[2]/div/div/section[3]/div[2]/div/div'

def click_checkin_old_style(driver):
    js = """
    var node = document.evaluate(
        '//*[@id="__next"]/div/div[3]/div[1]/ul/li[2]/div/div/section[3]/div[2]/div/div',
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    ).singleNodeValue;

    if (!node) return 'NOT_FOUND';

    try {
        node.click();
        return 'CLICK_NODE';
    } catch (e) {
        try {
            var ev = document.createEvent('MouseEvents');
            ev.initEvent('click', true, true);
            node.dispatchEvent(ev);
            return 'DISPATCH_EVENT';
        } catch (e2) {
            return 'FAILED';
        }
    }
    """
    return driver.execute_script(js)

class NexiraProject(BaseProject):
    name = 'nexira'

    def run(self, driver, profile):
        driver.get('https://www.nexira.ai/airdrops/campaigns')
        time.sleep(5)
        res = click_checkin_old_style(driver)
        print('CHECKIN:', res)
        time.sleep(3)
