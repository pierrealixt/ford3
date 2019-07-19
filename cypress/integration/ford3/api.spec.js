/// <reference types="Cypress" />

context('API', () => {
  it('should query the API', () => {
    cy.request('http://localhost/api/v1/providers')
      .then(response => {
        expect(response.body[0]).to.have.property('id')
      })
  })
})
