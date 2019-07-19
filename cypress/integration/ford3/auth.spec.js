/// <reference types="Cypress" />

context('Auth', () => {
  beforeEach(() => {
    cy.visit('http://localhost')
  })

  it('should not log in with a fake account', () => {
    cy.get('.text-right > .text-white')
      .click()

    cy.get('#id_username')
      .type('fake@email.com')

    cy.get('#id_password')
      .type('password')

    cy.get('.edu-button')
      .click()

    cy.contains('Please enter a correct email and password').should('be.visible')
    cy.get('#id_username')
      .should('have.value', 'fake@email.com')
  })

  it('should log in with a valid account', () => {
    cy.get('.text-right > .text-white')
      .click()

    cy.get('#id_username')
      .type('admin@admin.com')

    cy.get('#id_password')
      .type('admin')

    cy.get('.edu-button')
      .click()
    cy.url()
      .should('eq', 'http://localhost/dashboard/')

    cy.get(':nth-child(2) > .d-lg-block > .text-white')
      .contains('Dashboard')
  })
})
