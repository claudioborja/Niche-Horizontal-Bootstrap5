"""Exercise the template core with no jQuery or vendor JavaScript loaded."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


async def check_native(browser, base_url):
    context = await browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
    page = await context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    await page.set_content('''<html><body class="hold-transition fixed sidebar-mini">
<div class="wrapper"><header class="main-header" style="height:40px"></header>
<div class="menu-toggle"><button id="menu-btn">Navigation</button></div>
<ul id="respMenu" class="ace-responsive-menu" data-menu-style="horizontal">
<li><a href="#">First</a><ul><li><a href="#child">Child</a></li><li><a href="#">Nested</a><ul><li><a href="#deep">Deep</a></li></ul></li></ul></li>
<li><a href="#">Second</a><ul><li><a href="#other">Other</a></li></ul></li></ul>
<aside class="main-sidebar"><div class="sidebar">Sidebar</div></aside>
<div class="content-wrapper">
<div id="native-box" class="box" data-animation-speed="0"><div class="box-tools"><button data-widget="collapse">Toggle</button><button data-widget="remove">Remove</button></div><div class="box-body">Content</div><div class="box-footer">Footer</div></div>
<ul id="native-tree"><li class="treeview"><a href="#">One</a><ul class="treeview-menu" style="display:none"><li>Child</li></ul></li><li class="treeview"><a href="#">Two</a><ul class="treeview-menu" style="display:none"><li>Child</li></ul></li></ul>
<ul id="native-todo"><li><input type="checkbox" aria-label="Task"></li></ul>
<div class="direct-chat"><button data-widget="chat-pane-toggle">Chat</button></div>
<button data-toggle="push-menu">Sidebar</button><button data-toggle="control-sidebar">Settings</button><aside class="control-sidebar"></aside>
</div><footer class="main-footer" style="height:30px"></footer></div></body></html>''')
    await page.add_style_tag(url=base_url + '/assets/css/theme.css')
    await page.add_style_tag(url=base_url + '/assets/plugins/hmenu/ace-responsive-menu.css')
    for source in ('niche.js', 'niche/layout.js', 'niche/navigation.js', 'niche/widgets.js'):
        await page.add_script_tag(path=str(ROOT / 'assets/js' / source))
    assert await page.evaluate("typeof jQuery === 'undefined' && typeof $ === 'undefined'")
    assert await page.evaluate("!!Niche.getComponent(document.body, 'layout') && !document.body.classList.contains('hold-transition')")
    assert await page.locator('.sidebar').evaluate("el => el.style.overflowY === 'auto' && parseInt(el.style.height) === 960")
    branch = page.locator('#respMenu > li > a').first
    await branch.hover()
    assert await branch.get_attribute('aria-expanded') == 'true'
    await page.locator('#respMenu > li > a').nth(1).hover()
    assert await branch.get_attribute('aria-expanded') == 'false'
    await branch.focus()
    await branch.press('ArrowDown')
    assert await page.evaluate("document.activeElement.textContent === 'Child'")
    await page.keyboard.press('Escape')
    assert await branch.get_attribute('aria-expanded') == 'false'
    await page.set_viewport_size({'width': 390, 'height': 844})
    await page.wait_for_function("document.getElementById('respMenu').classList.contains('hide-menu')")
    assert await page.locator('#respMenu').evaluate("el => el.classList.contains('hide-menu')")
    await page.click('#menu-btn')
    assert await page.locator('#menu-btn').get_attribute('aria-expanded') == 'true'
    await branch.click()
    assert await branch.get_attribute('aria-expanded') == 'true'
    await branch.press('Space')
    assert await branch.get_attribute('aria-expanded') == 'false'
    await page.set_viewport_size({'width': 1440, 'height': 1000})
    await page.wait_for_function("!document.getElementById('respMenu').classList.contains('hide-menu')")
    assert await page.locator('#respMenu').is_visible()
    assert await page.locator('#respMenu .slide').count() == 0

    assert await page.evaluate('''() => {
        let events = 0;
        const box = document.getElementById('native-box');
        box.addEventListener('collapsed.boxwidget', () => events++);
        const first = Niche.component(box, 'boxWidget');
        if (first !== Niche.component(box, 'boxWidget') || first.options.animationSpeed !== 0) return false;
        box.querySelector('[data-widget=collapse]').click();
        if (!box.classList.contains('collapsed-box') || events !== 1) return false;
        box.querySelector('[data-widget=collapse]').click();
        if (box.classList.contains('collapsed-box')) return false;
        const tree = document.getElementById('native-tree');
        Niche.component(tree, 'tree', { animationSpeed: 0 });
        const links = tree.querySelectorAll('.treeview > a');
        links[0].click();
        if (!links[0].parentElement.classList.contains('menu-open')) return false;
        links[1].click();
        if (links[0].parentElement.classList.contains('menu-open') || !links[1].parentElement.classList.contains('menu-open')) return false;
        links[1].click();
        let checked = 0, unchecked = 0;
        Niche.component('#native-todo', 'todoList', {
            onCheck() { if (this instanceof HTMLInputElement) checked++; },
            onUnCheck() { unchecked++; }
        });
        const checkbox = document.querySelector('#native-todo input');
        checkbox.click(); checkbox.click();
        if (checked !== 1 || unchecked !== 1 || checkbox.closest('li').classList.contains('done')) return false;
        document.querySelector('[data-widget=chat-pane-toggle]').click();
        if (!document.querySelector('.direct-chat').classList.contains('direct-chat-contacts-open')) return false;
        document.querySelector('[data-toggle=push-menu]').click();
        if (!document.body.classList.contains('sidebar-collapse')) return false;
        document.querySelector('[data-toggle=push-menu]').click();
        const settings = document.querySelector('[data-toggle=control-sidebar]');
        settings.click();
        if (!document.querySelector('.control-sidebar').classList.contains('control-sidebar-open')) return false;
        settings.click();
        if (document.querySelector('.control-sidebar').classList.contains('control-sidebar-open')) return false;
        box.querySelector('[data-widget=remove]').click();
        return !document.getElementById('native-box');
    }''')
    await page.emulate_media(reduced_motion='no-preference')
    await page.evaluate('''() => {
        const box = document.createElement('div');
        box.id = 'rapid-box'; box.className = 'box';
        box.innerHTML = '<div class="box-body" style="height:100px">Animated content</div>';
        document.querySelector('.content-wrapper').append(box);
        const instance = Niche.component(box, 'boxWidget', {animationSpeed: 60});
        instance.collapse(); instance.expand(); instance.collapse();
    }''')
    await page.wait_for_function("document.getElementById('rapid-box').classList.contains('collapsed-box') && document.querySelector('#rapid-box .box-body').style.display === 'none'")
    await page.evaluate("Niche.component('#rapid-box', 'boxWidget', 'expand')")
    await page.wait_for_function("document.querySelector('#rapid-box .box-body').getBoundingClientRect().height === 100")
    await page.set_viewport_size({'width': 390, 'height': 844})
    await page.wait_for_function("document.getElementById('respMenu').classList.contains('hide-menu')")
    await page.click('#menu-btn')
    await page.set_viewport_size({'width': 1440, 'height': 1000})
    await page.wait_for_timeout(250)
    assert await page.locator('#respMenu').is_visible()
    assert await page.locator('#menu-btn').get_attribute('aria-expanded') == 'true'
    assert not errors, '\n'.join(errors)
    print('PASS: core works without jQuery: native layout/scrolling, hover/keyboard/mobile menu, accordion trees, boxes, tasks, chat and sidebars.', flush=True)
    await context.close()
