/* ===========================================
   AI-Solutions — Main JavaScript
   =========================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* ──────────────────────────────────────────
     1. NAVBAR SCROLL EFFECT
  ────────────────────────────────────────── */
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const onScroll = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ──────────────────────────────────────────
     2. ACTIVE NAV LINK
  ────────────────────────────────────────── */
  const currentFile = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentFile || (currentFile === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  /* ──────────────────────────────────────────
     3. HAMBURGER MENU
  ────────────────────────────────────────── */
  const hamburger = document.getElementById('hamburger');
  const navMenu   = document.getElementById('navMenu');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', function () {
      const open = navMenu.classList.toggle('open');
      hamburger.classList.toggle('open', open);
      hamburger.setAttribute('aria-expanded', open);
    });

    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });

    document.addEventListener('click', function (e) {
      if (navbar && !navbar.contains(e.target)) {
        navMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ──────────────────────────────────────────
     4. CONTACT FORM
     (handled server-side by Django; no JS interception)
  ────────────────────────────────────────── */

  /* ──────────────────────────────────────────
     5. ADMIN LOGIN
     (handled server-side by Django; no JS interception)
  ────────────────────────────────────────── */

  /* ──────────────────────────────────────────
     6. ADMIN DASHBOARD
  ────────────────────────────────────────── */

  /* ──────────────────────────────────────────
     8. SMOOTH SCROLL — anchor links
  ────────────────────────────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const id     = this.getAttribute('href');
      const target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
