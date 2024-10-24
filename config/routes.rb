Rails.application.routes.draw do
  resources :liquidations, only: [:create, :show]
end
