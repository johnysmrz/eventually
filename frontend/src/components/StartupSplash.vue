<template>
    <div class="startup-splash">
        <div class="logo-container">
        </div>
        <img class="logo" src="../assets/logo256.png" alt="Eventually Logo" />
        <h1 class="title">Skip the hassle, catch the event. Eventually...</h1>
        <div class="loadingio-spinner-ellipsis-nq4q5u6dq7r">
            <div class="ldio-x2uulkbinbj">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'StartupSplash',
};
</script>

<style scoped>
/* Colors
#fecd40 - yellow
#c42737 - red
#2f7979 - teal
#10273a - blue
*/

.startup-splash {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: #f5f7fa;
}

.logo-container {
    margin-bottom: 24px;
}

.logo {
    width: 100px;
    height: 100px;
}

.title {
    font-size: 2rem;
    font-weight: bold;
    color: #10273a;
}

@keyframes ldio-x2uulkbinbj {
    0% {
        transform: translate(12px, 80px) scale(0);
    }

    25% {
        transform: translate(12px, 80px) scale(0);
    }

    50% {
        transform: translate(12px, 80px) scale(1);
    }

    75% {
        transform: translate(80px, 80px) scale(1);
    }

    100% {
        transform: translate(148px, 80px) scale(1);
    }
}

@keyframes ldio-x2uulkbinbj-r {
    0% {
        transform: translate(148px, 80px) scale(1);
    }

    100% {
        transform: translate(148px, 80px) scale(0);
    }
}

@keyframes ldio-x2uulkbinbj-c {
    0% {
        background: #fecd40
    }

    25% {
        background: #10273a
    }

    50% {
        background: #2f7979
    }

    75% {
        background: #c42737
    }

    100% {
        background: #fecd40
    }
}

.ldio-x2uulkbinbj div {
    position: absolute;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    transform: translate(80px, 80px) scale(1);
    background: #fecd40;
    animation: ldio-x2uulkbinbj 2.2222222222222223s infinite cubic-bezier(0, 0.5, 0.5, 1);
}

.ldio-x2uulkbinbj div:nth-child(1) {
    background: #c42737;
    transform: translate(148px, 80px) scale(1);
    animation: ldio-x2uulkbinbj-r 0.5555555555555556s infinite cubic-bezier(0, 0.5, 0.5, 1), ldio-x2uulkbinbj-c 2.2222222222222223s infinite step-start;
}

.ldio-x2uulkbinbj div:nth-child(2) {
    animation-delay: -0.5555555555555556s;
    background: #fecd40;
}

.ldio-x2uulkbinbj div:nth-child(3) {
    animation-delay: -1.1111111111111112s;
    background: #c42737;
}

.ldio-x2uulkbinbj div:nth-child(4) {
    animation-delay: -1.6666666666666665s;
    background: #2f7979;
}

.ldio-x2uulkbinbj div:nth-child(5) {
    animation-delay: -2.2222222222222223s;
    background: #10273a;
}

.loadingio-spinner-ellipsis-nq4q5u6dq7r {
    width: 200px;
    height: 200px;
    display: inline-block;
    overflow: hidden;
    background: none;
}

.ldio-x2uulkbinbj {
    width: 100%;
    height: 100%;
    position: relative;
    transform: translateZ(0) scale(1);
    backface-visibility: hidden;
    transform-origin: 0 0;
    /* see note above */
}

.ldio-x2uulkbinbj div {
    box-sizing: content-box;
}
</style>