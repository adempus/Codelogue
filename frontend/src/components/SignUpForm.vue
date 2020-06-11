<template>
    <Card id="signup_card">
        <template slot="content">
            <div class="p-fluid p-formgrid p-grid p-justify-center">
                <div class="p-field p-col-6">
                    <InputText v-model="firstName"
                            id="first_name" placeholder="First Name" type="text" />
                </div>
                <div class="p-field p-col-6">
                    <InputText v-model="lastName"
                            id="last_name" placeholder="Last Name" type="text" />
                </div>
                <div class="p-field p-col-12">
                    <InputText v-model="username"
                            id="username" placeholder="Username" type="text" />
                </div>
                <div class="p-field p-col-12">
                    <InputText v-model="email"
                            id="email" placeholder="Email" type="email" />
                </div>
                <div class="p-field p-col-6">
                    <InputText v-model="password"
                            id="password" placeholder="Password" type="password" />
                </div>
                <div class="p-field p-col-6">
                    <InputText v-model="confirmPass"
                            id="confirm_pass" placeholder="Confirm Password" type="password" />
                </div>
                <Button type="button" label="Sign Up" class="p-button-sm " id="signup_btn"/>
            </div>
        </template>
    </Card>
</template>

<script>
export default {
  name: 'SignUpForm',
  data: () => {
    return {
      firstName: '',
      lastName: '',
      username: '',
      email: '',
      password: '',
      confirmPass: '',
      response: {},
    };
  },
};
</script>

<style scoped>
    #signup_card {
        width: auto;
        background-color: #272a36;
        border-radius: 5px;
        padding: 10px 15px 10px 15px;
    }

    #signup_card input {
        border-radius: 5px;
        background-color: #323645;
        border-color: #323645;
        color: #FFFFFF;
        margin-bottom: 12px;
        font-family: 'Open Sans', sans-serif;
    }

    #signup_btn {
        background-color: #DB564E;
        border-color: #DB564E;
        margin-top: 10px;
        width: 165px;
        font-family: 'Open Sans', sans-serif;
    }
</style>
