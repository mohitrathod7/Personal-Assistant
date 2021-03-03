/* Display Nav */
function openNav() {
    document.getElementById("mySidepanel").style.width = "250px";
}

const sidePanel = gsap.timeline({ defaults: {duration: 1 }});

$('.fa-bars').click(function(){
    sidePanel
        .from('#mySidepanel a', { ease: 'power2.in', duration: 0.4, x: -300, stagger: 0.15 })
})


$('.closebtn').click(function(){        
    function hidepanel() {
        document.getElementById("mySidepanel").style.width = "0";
    }

    sidePanel
        .to('#mySidepanel a', { ease: 'power2.in', duration: 0.4, x: -300, stagger: 0.15 })
        .to('#mySidepanel a', { ease: 'power2.in', duration: 0.4, x: 0 })
    
    setTimeout(hidepanel, 1000);
})
