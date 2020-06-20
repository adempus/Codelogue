<template>
    <div class="p-grid p-justify-center">
        <div class="p-col-12 p-lg-6 header_section">
            <p class="header">Remember<br> Your Lines</p>
            <p class="info">Simple code snippet and <br> documentation tool.</p>
        </div>
        <div class="p-col-12 p-lg-4 p-sm-6 signup_section">
            <SignUpForm></SignUpForm>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Landing'
};
</script>

<style scoped>
    .header_section {
        text-align: center;
        padding-top: 7%;
    }

    .signup_section {
        padding-top: 13%;
        width: 30%;
    }
    @media(max-width: 1450px) {
        .signup_section {
            padding: 75px 295px 75px 295px;
            width: 100%;
        }
    }
    @media(max-width: 1024px) {
        .signup_section {
            padding: 10vh 7vh 5vh 7vh;
            width: 100%;
        }
    }
    .header {
        position:relative;
        left: 0;
        font-size: 650%;
        color: #DB564E;
        font-family: 'NTR', sans-serif;
        margin-bottom: 5px;
        font-weight: 500;
        line-height: 0.9em;
    }

    @media(min-width: 690px) {
        .header { font-size: 7em; }
    }
    @media(max-width: 420px) {
        .header { font-size: 5.5em; }
    }
    @media(max-width: 290px) {
        .header { font-size: 0.5em; }
    }

    .info {
        font-size: 24px;
        color: #FFFFFF;
        font-family: 'Open Sans', sans-serif;
        font-weight: 500;
        letter-spacing: 5px;
        padding-left: 3%;
    }
</style>
