/**
 * Extra JavaScript for MkDocs Advanced Template
 * Enhanced interactive features and user experience improvements
 */

(function() {
  'use strict';

  // Wait for DOM to be ready
  document.addEventListener('DOMContentLoaded', function() {
    console.log('MkDocs Advanced Template - Custom scripts loaded successfully.');
    
    // Initialize all enhancements
    initializeScrollEnhancements();
    initializeTableEnhancements();
    initializeCodeEnhancements();
    initializeMermaidEnhancements();
    initializeSearchEnhancements();
    initializeNavigationEnhancements();
    initializeThemeEnhancements();
    initializeAccessibilityEnhancements();
  });

  /**
   * Enhanced scrolling features
   */
  function initializeScrollEnhancements() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });

    // Add scroll-to-top button
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '↑';
    scrollToTopBtn.className = 'scroll-to-top';
    scrollToTopBtn.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 50px;
      height: 50px;
      border: none;
      border-radius: 50%;
      background: var(--md-primary-fg-color);
      color: white;
      font-size: 18px;
      cursor: pointer;
      opacity: 0;
      transition: all 0.3s ease;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;

    document.body.appendChild(scrollToTopBtn);

    // Show/hide scroll-to-top button
    window.addEventListener('scroll', function() {
      if (window.pageYOffset > 300) {
        scrollToTopBtn.style.opacity = '1';
        scrollToTopBtn.style.transform = 'scale(1)';
      } else {
        scrollToTopBtn.style.opacity = '0';
        scrollToTopBtn.style.transform = 'scale(0.8)';
      }
    });

    scrollToTopBtn.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  /**
   * Enhanced table features
   */
  function initializeTableEnhancements() {
    // Make tables responsive
    document.querySelectorAll('table').forEach(table => {
      if (!table.closest('.md-typeset')) return;
      
      const wrapper = document.createElement('div');
      wrapper.className = 'table-wrapper';
      wrapper.style.cssText = `
        overflow-x: auto;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      `;
      
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
      
      // Add sortable functionality to tables
      addTableSorting(table);
    });
  }

  /**
   * Add sorting functionality to tables
   */
  function addTableSorting(table) {
    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
      header.style.cursor = 'pointer';
      header.style.userSelect = 'none';
      header.addEventListener('click', function() {
        sortTable(table, index);
      });
    });
  }

  /**
   * Sort table by column
   */
  function sortTable(table, columnIndex) {
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const header = table.querySelectorAll('th')[columnIndex];
    const isAscending = header.dataset.sorted !== 'asc';
    
    rows.sort((a, b) => {
      const aText = a.cells[columnIndex].textContent.trim();
      const bText = b.cells[columnIndex].textContent.trim();
      
      // Try to parse as numbers
      const aNum = parseFloat(aText);
      const bNum = parseFloat(bText);
      
      if (!isNaN(aNum) && !isNaN(bNum)) {
        return isAscending ? aNum - bNum : bNum - aNum;
      }
      
      // String comparison
      return isAscending ? aText.localeCompare(bText) : bText.localeCompare(aText);
    });
    
    // Update header indicators
    table.querySelectorAll('th').forEach(th => {
      th.dataset.sorted = '';
      th.style.position = 'relative';
    });
    
    header.dataset.sorted = isAscending ? 'asc' : 'desc';
    header.style.position = 'relative';
    
    // Add visual indicator
    const indicator = header.querySelector('.sort-indicator') || document.createElement('span');
    indicator.className = 'sort-indicator';
    indicator.innerHTML = isAscending ? ' ↑' : ' ↓';
    indicator.style.cssText = `
      position: absolute;
      right: 8px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 12px;
      color: var(--md-accent-fg-color);
    `;
    
    if (!header.querySelector('.sort-indicator')) {
      header.appendChild(indicator);
    }
    
    // Re-append sorted rows
    const tbody = table.querySelector('tbody');
    rows.forEach(row => tbody.appendChild(row));
  }

  /**
   * Enhanced code block features
   */
  function initializeCodeEnhancements() {
    // Add copy button to code blocks
    document.querySelectorAll('pre code').forEach(codeBlock => {
      const pre = codeBlock.parentElement;
      if (pre.querySelector('.copy-btn')) return; // Already has copy button
      
      const copyBtn = document.createElement('button');
      copyBtn.className = 'copy-btn';
      copyBtn.innerHTML = '📋';
      copyBtn.title = 'Copy code';
      copyBtn.style.cssText = `
        position: absolute;
        top: 8px;
        right: 8px;
        background: var(--md-accent-fg-color);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 4px 8px;
        cursor: pointer;
        font-size: 12px;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1;
      `;
      
      pre.style.position = 'relative';
      pre.appendChild(copyBtn);
      
      // Show copy button on hover
      pre.addEventListener('mouseenter', () => {
        copyBtn.style.opacity = '1';
      });
      
      pre.addEventListener('mouseleave', () => {
        copyBtn.style.opacity = '0';
      });
      
      // Copy functionality
      copyBtn.addEventListener('click', function() {
        navigator.clipboard.writeText(codeBlock.textContent).then(() => {
          copyBtn.innerHTML = '✓';
          copyBtn.style.background = 'var(--md-accent-fg-color)';
          setTimeout(() => {
            copyBtn.innerHTML = '📋';
            copyBtn.style.background = 'var(--md-accent-fg-color)';
          }, 2000);
        });
      });
    });
  }

  /**
   * Enhanced Mermaid diagram features
   */
  function initializeMermaidEnhancements() {
    // Wait for Mermaid to load
    if (typeof mermaid !== 'undefined') {
      // Configure Mermaid theme based on current theme
      const isDarkMode = document.querySelector('[data-md-color-scheme="slate"]');
      
      mermaid.initialize({
        theme: isDarkMode ? 'dark' : 'base',
        themeVariables: {
          primaryColor: getComputedStyle(document.documentElement).getPropertyValue('--md-primary-fg-color'),
          primaryTextColor: getComputedStyle(document.documentElement).getPropertyValue('--md-custom-text'),
          primaryBorderColor: getComputedStyle(document.documentElement).getPropertyValue('--md-primary-fg-color--dark'),
          lineColor: getComputedStyle(document.documentElement).getPropertyValue('--md-custom-text'),
          secondaryColor: getComputedStyle(document.documentElement).getPropertyValue('--md-accent-fg-color'),
          tertiaryColor: '#f5f5f5'
        }
      });
    }
    
    // Add fullscreen functionality to Mermaid diagrams
    document.querySelectorAll('.mermaid').forEach(diagram => {
      diagram.addEventListener('click', function() {
        toggleFullscreen(this);
      });
      
      diagram.style.cursor = 'pointer';
      diagram.title = 'Click to expand';
    });
  }

  /**
   * Toggle fullscreen for elements
   */
  function toggleFullscreen(element) {
    if (element.classList.contains('fullscreen')) {
      element.classList.remove('fullscreen');
      element.style.cssText = element.dataset.originalStyle || '';
      document.body.style.overflow = '';
    } else {
      element.dataset.originalStyle = element.style.cssText;
      element.classList.add('fullscreen');
      element.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: var(--md-custom-bg);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        box-sizing: border-box;
      `;
      document.body.style.overflow = 'hidden';
    }
  }

  /**
   * Enhanced search features
   */
  function initializeSearchEnhancements() {
    // Add search keyboard shortcuts
    document.addEventListener('keydown', function(e) {
      // Ctrl/Cmd + K to focus search
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.md-search__input');
        if (searchInput) {
          searchInput.focus();
        }
      }
      
      // Escape to close search
      if (e.key === 'Escape') {
        const searchInput = document.querySelector('.md-search__input');
        if (searchInput && document.activeElement === searchInput) {
          searchInput.blur();
        }
      }
    });
  }

  /**
   * Enhanced navigation features
   */
  function initializeNavigationEnhancements() {
    // Add breadcrumb navigation
    addBreadcrumbs();
    
    // Add reading progress indicator
    addReadingProgress();
    
    // Add table of contents highlighting
    addTocHighlighting();
  }

  /**
   * Add breadcrumb navigation
   */
  function addBreadcrumbs() {
    const content = document.querySelector('.md-content');
    if (!content) return;
    
    const breadcrumbs = document.createElement('nav');
    breadcrumbs.className = 'breadcrumbs';
    breadcrumbs.style.cssText = `
      padding: 1rem 0;
      font-size: 0.875rem;
      color: var(--md-custom-text-light);
    `;
    
    const path = window.location.pathname.split('/').filter(Boolean);
    let breadcrumbHTML = '<a href="/">Home</a>';
    
    let currentPath = '';
    path.forEach((segment, index) => {
      currentPath += '/' + segment;
      const isLast = index === path.length - 1;
      const displayName = segment.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      
      if (isLast) {
        breadcrumbHTML += ` / <span>${displayName}</span>`;
      } else {
        breadcrumbHTML += ` / <a href="${currentPath}">${displayName}</a>`;
      }
    });
    
    breadcrumbs.innerHTML = breadcrumbHTML;
    content.insertBefore(breadcrumbs, content.firstChild);
  }

  /**
   * Add reading progress indicator
   */
  function addReadingProgress() {
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 0;
      height: 3px;
      background: var(--md-accent-fg-color);
      z-index: 1000;
      transition: width 0.3s ease;
    `;
    
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', function() {
      const scrollTop = window.pageYOffset;
      const docHeight = document.body.scrollHeight - window.innerHeight;
      const scrollPercent = (scrollTop / docHeight) * 100;
      
      progressBar.style.width = scrollPercent + '%';
    });
  }

  /**
   * Add table of contents highlighting
   */
  function addTocHighlighting() {
    const headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    const tocLinks = document.querySelectorAll('.md-nav__link');
    
    if (headers.length === 0 || tocLinks.length === 0) return;
    
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            if (id) {
              tocLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + id) {
                  link.classList.add('active');
                }
              });
            }
          }
        });
      },
      { threshold: 0.5 }
    );
    
    headers.forEach(header => {
      if (header.id) {
        observer.observe(header);
      }
    });
  }

  /**
   * Enhanced theme features
   */
  function initializeThemeEnhancements() {
    // Add theme transition animations
    const style = document.createElement('style');
    style.textContent = `
      * {
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
      }
    `;
    document.head.appendChild(style);
    
    // Listen for theme changes
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-md-color-scheme') {
          // Re-initialize Mermaid with new theme
          if (typeof mermaid !== 'undefined') {
            const isDarkMode = document.querySelector('[data-md-color-scheme="slate"]');
            mermaid.initialize({
              theme: isDarkMode ? 'dark' : 'base'
            });
          }
        }
      });
    });
    
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['data-md-color-scheme']
    });
  }

  /**
   * Enhanced accessibility features
   */
  function initializeAccessibilityEnhancements() {
    // Add skip links
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    skipLink.style.cssText = `
      position: absolute;
      top: -40px;
      left: 6px;
      background: var(--md-primary-fg-color);
      color: white;
      padding: 8px;
      text-decoration: none;
      border-radius: 4px;
      z-index: 1000;
      transition: top 0.3s ease;
    `;
    
    skipLink.addEventListener('focus', function() {
      this.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', function() {
      this.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add main content landmark
    const mainContent = document.querySelector('.md-content');
    if (mainContent) {
      mainContent.id = 'main-content';
      mainContent.setAttribute('role', 'main');
    }
    
    // Enhance focus indicators
    const focusStyle = document.createElement('style');
    focusStyle.textContent = `
      *:focus {
        outline: 2px solid var(--md-accent-fg-color);
        outline-offset: 2px;
      }
      
      .skip-link:focus {
        outline: 2px solid white;
      }
    `;
    document.head.appendChild(focusStyle);
  }

  // Print enhancements
  window.addEventListener('beforeprint', function() {
    // Expand all collapsible sections for printing
    document.querySelectorAll('details').forEach(details => {
      details.open = true;
    });
  });

  // Performance monitoring
  if ('performance' in window) {
    window.addEventListener('load', function() {
      setTimeout(function() {
        const perfData = performance.getEntriesByType('navigation')[0];
        console.log('Page load time:', perfData.loadEventEnd - perfData.fetchStart, 'ms');
      }, 0);
    });
  }

})();
