const home = gsap.timeline({ defaults: {duration: 1 }});

home
    .from('h1', { opacity: 0, duration: 1})
    .from('#search-bar', {x: '-200%', ease: 'bounce', duration: 1})
    .from('.button', {x: '800%', ease: 'bounce', duration: 1, stagger: 0.5})
