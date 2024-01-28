/*!
* Start Bootstrap - Creative v7.0.7 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Activate SimpleLightbox plugin for portfolio items
    new SimpleLightbox({
        elements: '#portfolio a.portfolio-box'
    });

});

// chat functions
const chatBox = document.getElementById('chatBox');
const audioInput = document.getElementById('audioInput');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const uploadInput = document.getElementById('uploadInput');
const downloadButton = document.getElementById('downloadButton');

sendButton.addEventListener('click', () => {
    const messageText = messageInput.value;
    if (messageText.trim() !== '') {
    addMessage('text', messageText);
    messageInput.value = '';
    }
});

audioInput.addEventListener('change', (event) => {
const audioFile = event.target.files[0];
if (audioFile) {
    addMessage('audio', audioFile);
    }
});

uploadInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
    displayImage(file);
    }
});

chatBox.addEventListener('click', (event) => {
    const clickedMessage = event.target;
    if (clickedMessage.classList.contains('message')) {
    clickedMessage.classList.toggle('selected');
    }
});

downloadButton.addEventListener('click', () => {
    const selectedMessages = Array.from(document.querySelectorAll('.message.selected'));
    if (selectedMessages.length > 0) {
    const selectedContent = selectedMessages.map(message => message.textContent).join('\n');
    const blob = new Blob([selectedContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'selected_content.txt';
    a.click();
    URL.revokeObjectURL(url);
    }
});

function addMessage(type, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    if (type === 'text') {
    messageDiv.textContent = content;
    } else if (type === 'audio') {
    const audio = document.createElement('audio');
    audio.controls = true;
    audio.src = URL.createObjectURL(content);
    messageDiv.appendChild(audio);
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

function displayImage(file) {
    const imageDiv = document.createElement('div');
    imageDiv.className = 'message';
    const image = document.createElement('img');
    image.src = URL.createObjectURL(file);
    image.style.maxWidth = '100%';
    imageDiv.appendChild(image);
    chatBox.appendChild(imageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}
