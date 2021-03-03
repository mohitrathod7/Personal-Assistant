const nav = gsap.timeline({ defaults: {duration: 1 }});

nav
    .from('.left-link', { ease: 'bounce', duration: 0.5, x: -200, stagger: 0.5})
    .from('.right-link', { ease: 'bounce', duration: 0.5, x: 200, stagger: 0.5})
