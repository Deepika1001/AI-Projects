package com.ecommerce.orderservice.controller;

import com.ecommerce.orderservice.model.Order;
import com.ecommerce.orderservice.service.OrderService;
import org.springframework.web.bind.annotation.*;

/**
 * REST controller for order operations used by agentic ecommerce assistant.
 */
@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    /**
     * Fetch complete order data by id.
     */
    @GetMapping("/{id}")
    public Order getOrder(@PathVariable String id) {
        return service.getOrder(id);
    }

    /**
     * Retrieve current order status.
     */
    @GetMapping("/{id}/status")
    public String getOrderStatus(@PathVariable String id) {
        return service.getOrderStatus(id);
    }

    /**
     * Update the shipping address for an order.
     */
    @PutMapping("/{id}/address")
    public Order updateAddress(@PathVariable String id, @RequestParam String address) {
        return service.updateAddress(id, address);
    }
}