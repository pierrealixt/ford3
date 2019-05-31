/// <reference types="Cypress" />

context('Auth', () => {
  beforeEach(() => {
    cy.visit('http://localhost')
  })

  it('.type() - type into a DOM element', () => {
    cy.get('.text-right > .text-white')
      .click()

    cy.get('#id_username')
      .type('fake@email.com')

    cy.get('#id_password')
      .type('password')

    cy.get('.edu-button')
      .click()
    cy.get('#login-form')
      .should(
        'contain',
        'Please enter a correct username and password.'
      )

    cy.get('#id_username')
      .should('have.value', 'fake@email.com')
  })
})
