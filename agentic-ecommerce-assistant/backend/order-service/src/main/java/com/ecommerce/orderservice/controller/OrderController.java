package com.ecommerce.orderservice.controller;

import com.ecommerce.orderservice.model.Order;
import com.ecommerce.orderservice.service.OrderService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    @GetMapping("/{id}")
    public Order getOrder(@PathVariable String id) {
        return service.getOrder(id);
    }

    @GetMapping("/{id}/status")
    public String getOrderStatus(@PathVariable String id) {
        return service.getOrderStatus(id);
    }

    @PutMapping("/{id}/address")
    public Order updateAddress(@PathVariable String id, @RequestParam String address) {
        return service.updateAddress(id, address);
    }
}