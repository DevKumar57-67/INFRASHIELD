document.addEventListener('DOMContentLoaded', function () {
    const storageKey = 'infraShieldSidebarState';
    const body = document.body;
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const navToggle = document.getElementById('nav-toggle');
    const backdrop = document.getElementById('sidebar-backdrop');

    function applyCollapsedState(isCollapsed) {
        body.classList.toggle('sidebar-collapsed', isCollapsed);
        localStorage.setItem(storageKey, isCollapsed ? 'collapsed' : 'expanded');
    }

    function syncSidebarState() {
        const saved = localStorage.getItem(storageKey);
        if (saved === 'collapsed') {
            applyCollapsedState(true);
            return;
        }
        applyCollapsedState(false);
    }

    function setMobileSidebar(open) {
        if (window.innerWidth > 960) return;
        body.classList.toggle('mobile-sidebar-open', open);
    }

    function handleToggle() {
        if (window.innerWidth > 960) {
            const isCollapsed = body.classList.contains('sidebar-collapsed');
            applyCollapsedState(!isCollapsed);
            return;
        }

        const isOpen = body.classList.contains('mobile-sidebar-open');
        setMobileSidebar(!isOpen);
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', handleToggle);
    }

    if (navToggle) {
        navToggle.addEventListener('click', handleToggle);
    }

    if (backdrop) {
        backdrop.addEventListener('click', function () {
            setMobileSidebar(false);
        });
    }

    window.addEventListener('resize', function () {
        if (window.innerWidth > 960) {
            body.classList.remove('mobile-sidebar-open');
        }
    });

    syncSidebarState();
});
